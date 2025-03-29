import requests
import pandas as pd
import bs4
import os
from concurrent.futures import ThreadPoolExecutor
import glob

url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
path = "/Users/william/Documents/data-engineering-practice/Exercises/Exercise-2/downloads"

def download_csv(url):
    """Função para baixar um arquivo CSV a partir de uma URL."""
    tgt_file = os.path.join(path, url.split("/")[-1])
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Verifica se houve erro na requisição
        
        with open(tgt_file, "wb") as file:
            file.write(response.content)
        return tgt_file  # Retorna o caminho do arquivo baixado
    
    except requests.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")
        return None  # Retorna None se falhar

def main():
    # Criar diretório de downloads, se não existir
    os.makedirs(path, exist_ok=True)
    print(f"Folder {path} exists or has been created.")
    
    # Obtendo a página HTML
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    
    # Encontrando todas as linhas da tabela
    rows = soup.findAll("tr")
    filtered_urls = []

    # Filtrando os arquivos com o timestamp desejado
    for row in rows:
        columns = row.findAll("td")
        if len(columns) >= 2:
            file_name = columns[0].find("a").text.strip()
            timestamp_str = columns[1].text.strip()

            if timestamp_str == "2024-01-19 10:27":
                filtered_urls.append(url + file_name)

    print(f"Arquivos encontrados para o timestamp desejado: {len(filtered_urls)}")

    # Definir o número de threads
    num_threads = 10  

    # Baixando os arquivos em paralelo
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        downloaded_files = list(executor.map(download_csv, filtered_urls))

    # Removendo arquivos que não foram baixados corretamente
    downloaded_files = [file for file in downloaded_files if file is not None]

    if not downloaded_files:
        print("Nenhum arquivo foi baixado com sucesso. Encerrando.")
        return

    print(f"{len(downloaded_files)} arquivos foram baixados com sucesso.")

    # Lista para armazenar os DataFrames
    listfile = []

    # Lendo os arquivos CSV e pegando a coluna 'HourlyDryBulbTemperature'
    for file in downloaded_files:
        try:
            df = pd.read_csv(file, dtype=object, skiprows=1, usecols=[10], names=['HourlyDryBulbTemperature'])
            df['HourlyDryBulbTemperature'] = pd.to_numeric(df['HourlyDryBulbTemperature'], errors='coerce')  # Converte para float
            listfile.append(df)
        except Exception as e:
            print(f"Erro ao ler {file}: {e}")

    # Concatenando todos os DataFrames
    if listfile:
        full_df = pd.concat(listfile, axis=0, ignore_index=True)

        # Removendo valores nulos antes de calcular o máximo
        full_df = full_df.dropna(subset=['HourlyDryBulbTemperature'])

        # Encontrando a temperatura máxima
        max_temp = full_df['HourlyDryBulbTemperature'].max()

        # Filtrando os registros com essa temperatura
        max_temp_records = full_df[full_df['HourlyDryBulbTemperature'] == max_temp]

        # Exibir resultados
        print(f"\nA maior temperatura registrada foi: {max_temp}")
        print("Registros correspondentes:")
        print(max_temp_records)
    else:
        print("Nenhum dado válido encontrado.")

if __name__ == "__main__":
    main()
