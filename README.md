
# Script para Busca e Extração de Dados de Proteínas do NCBI

## Descrição

O script `ncbi_protein_search.py` é uma ferramenta Python que realiza buscas em bases de dados do NCBI para extrair informações sobre proteínas. Usando termos de busca fornecidos por um arquivo de entrada, o script acessa as APIs `esearch` e `efetch` do NCBI para realizar as buscas e recuperar os dados. Os resultados são então salvos em um arquivo CSV.

## Funcionalidades

- Busca de proteínas em bases de dados do NCBI usando termos de busca específicos.
- Extração de informações sobre produtos de proteínas e IDs de proteínas.
- Geração de um arquivo CSV com os resultados da busca.

## Requisitos

- Python 3.x
- Bibliotecas Python: `requests`, `xml.etree.ElementTree`, `re`, `argparse`, `os`

## Instalação

Para instalar e configurar o script em sua máquina local, siga as instruções abaixo:

1. Clone este repositório:
   ```bash
   git clone https://github.com/BiazzMoura/ncbi_protein_search.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd ncbi_protein_search
   ```

3. Instale as dependências necessárias (se não estiverem instaladas):
   ```bash
   pip install requests
   ```

## Uso

Para usar o script, siga os passos abaixo:

1. Prepare um arquivo de texto contendo os termos de busca, um termo por linha. Por exemplo:
   ```
   term1
   term2
   term3
   ```

2. Execute o script fornecendo o caminho para o arquivo de entrada como argumento:
   ```bash
   python ncbi_protein_search.py termos_de_busca.txt
   ```

3. O script irá gerar um arquivo CSV contendo os termos de busca, produtos das proteínas e IDs das proteínas no diretório de trabalho atual.

## Exemplo

### Arquivo de Entrada: `termos_de_busca.txt`
```
locus_tag1
locus_tag2
locus_tag3
```

### Execução do Script
```bash
python ncbi_protein_search.py termos_de_busca.txt
```

### Saída Esperada
Um arquivo CSV chamado `termos_de_busca_results.csv` contendo os resultados da busca.


