#!/bin/python
import requests
import xml.etree.ElementTree as ET
import re
import argparse
import os

# URLs da API do NCBI para buscas e recuperação de dados
NCBI_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_protein(search_name, content):
    """
    Busca a tradução e outros detalhes de uma proteína com base no nome fornecido.

    Args:
        search_name (str): Nome do locus a ser pesquisado.
        content (str): Conteúdo do GenBank para busca.

    Returns:
        tuple: Produto da proteína e ID da proteína.
    """
    # Busca pelo locus_tag e pela tradução da proteína
    match = re.search(r'/(?:old_)?locus_tag="{}"((?:\s|.)*?)/translation'.format(search_name), content)
    if not match or not all(match.groups()):
        raise ValueError

    CDS_content = match.group(1)
    product_match = re.search(r'/product="((.|\s)*?)"', CDS_content)
    protein_id_match = re.search(r'/protein_id="((.|\s)*?)"', CDS_content)
    
    product = product_match.group(1) if product_match and all(product_match.groups()) else ""
    protein_id = protein_id_match.group(1) if protein_id_match and all(protein_id_match.groups()) else ""

    return product, protein_id

def fetch_data(db_id, db="nuccore", retmode="text", rettype="gbwithparts"):
    """
    Recupera dados do NCBI com base no ID fornecido.

    Args:
        db_id (str): ID do banco de dados do NCBI.
        db (str): Nome do banco de dados a ser pesquisado (padrão é 'nuccore').
        retmode (str): Modo de retorno dos dados (padrão é 'text').
        rettype (str): Tipo de retorno dos dados (padrão é 'gbwithparts').

    Returns:
        bytes: Conteúdo dos dados recuperados.
    """
    params = {
        "id": db_id,
        "db": db,
        "retmode": retmode,
        "rettype": rettype,
    }
    print("Fetching data for https://www.ncbi.nlm.nih.gov/nuccore/{}. It may take a while.".format(db_id))
    resp = requests.get(NCBI_EFETCH, params)
    return resp.content

def search_term(term, database="nuccore"):
    """
    Realiza uma busca no NCBI usando um termo específico.

    Args:
        term (str): Termo a ser pesquisado.
        database (str): Banco de dados a ser pesquisado (padrão é 'nuccore').

    Returns:
        list: Lista contendo o produto da proteína e ID da proteína, ou uma lista vazia se nada for encontrado.
    """
    search_term = {
        "db": database,
        "term": term,
    }

    resp = requests.get(NCBI_ESEARCH, search_term)
    et = ET.fromstring(resp.content)
    results = et.findall("./IdList/Id")
    
    if not results:
        print("No results found")
        return
    
    print("Results found in:")
    for result_id in results:
        print("https://www.ncbi.nlm.nih.gov/nuccore/{}/".format(result_id.text))
    
    print("")
    for result_id in results:
        _id = result_id.text
        content = fetch_data(_id).decode("utf-8")
        for subterm in term.split("|"):
            try:
                print(f"Searching for {subterm} in ID: {_id}")
                return search_protein(subterm, content)
            except ValueError:
                print(f"No data found in https://www.ncbi.nlm.nih.gov/nuccore/{_id} for {subterm}")
    return ["", ""]

def main():
    """
    Função principal que lida com a leitura de arquivos de entrada, realiza buscas e salva os resultados em um arquivo CSV.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, nargs="?", help="Input file")
    args = parser.parse_args()

    if args.file:
        term_file = args.file
    else:
        term_file = input("Input file: ")

    # Extrair o nome do arquivo sem a extensão
    file_name, _ = os.path.splitext(os.path.basename(term_file))

    # Ler termos do arquivo de entrada
    with open(term_file) as f:
        terms = [term.rstrip() for term in f.readlines()]

    results = []

    # Realizar busca para cada termo
    for term in terms:
        term_results = search_term(term)
        if term_results:
            results.append([term] + list(term_results))
        else:
            print(f"No results found for {term}")

    # Definir o caminho do arquivo de saída usando o diretório de trabalho atual
    output_file = os.path.join(os.getcwd(), f"{file_name}_results.csv")

    # Salvar os resultados em um arquivo CSV
    try:
        with open(output_file, "w") as f:
            f.write("term,product,protein_id\n")
            for term, product, protein_id in results:
                f.write(f"{term},{product},{protein_id}\n")
        print(f"Output file {output_file} successfully created.")
    except Exception as e:
        print(f"Error creating output file {output_file}: {e}")

if __name__ == "__main__":
    main()
