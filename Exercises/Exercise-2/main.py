import requests
import pandas as pd
import bs4
import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import glob

url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
path = "/Users/william/Documents/data-engineering-practice/Exercises/Exercise-2/downloads"

def download_csv(url):
        tgt_file = os.path.join(path ,url.split("/")[-1])
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()  # Lança um erro se a requisição falhar
            
            with open(tgt_file, "wb") as file:
                    file.write(response.content)
            return f"Arquivo baixado: {tgt_file}"
        
        except requests.RequestException as e:
            return f"Erro ao baixar {url}: {e}"


def main():

    os.makedirs(path, exist_ok=True)
    print(f"Folder {path} exists or has been created.")
    response = requests.get(url)
    #print(response.text)
    html = response.content
    soup = bs4.BeautifulSoup(html,"html.parser")
    #print(soup.prettify())
    rows = soup.findAll("tr")
    #print(span_elements)

    filtered_urls = []


    for i in rows:
        columns = i.findAll("td")
        if len(columns) >= 2:
        #    print(columns[0].find("a").text.strip())
            file_name = columns[0].find("a").text.strip()
            timestamp_str = columns[1].text.strip()
            #print(file_name + ' ' + timestamp_str)

            if timestamp_str == "2024-01-19 10:27":
                filtered_urls.append(url+file_name)
#               print(filtered_urls)


    # Define o número de threads (ajuste conforme necessário)
    num_threads = 10  

    # Baixando os arquivos em paralelo
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(download_csv, filtered_urls))

    # Exibir os resultados
#    for result in results:
#        print(result)            
    

    tgt_file = glob.glob(os.path.join(path ,"*.csv"))
    #print(tgt_file)

    listfile = []

    for file in tgt_file:
        df = pd.read_csv(file, dtype=object, skiprows=1,usecols=[10], names=['HourlyDryBulbTemperature'])
        df['HourlyDryBulbTemperature'] = pd.to_numeric(df['HourlyDryBulbTemperature'], errors='coerce')
        listfile.append(df) 
    #print(listfile)
    #print(listfile)
    frame = pd.concat(listfile, axis=0)
    #frame_float = pd.to_numeric(frame)
    max_temp = frame['HourlyDryBulbTemperature'].max()
    print(max_temp)
    #print(frame['HourlyDryBulbTemperature'].max())
    #max_HourlyDryBulbTemperature = frame.max('HourlyDryBulbTemperature')
    #print(frame.max("HourlyDryBulbTemperature"))
pass


if __name__ == "__main__":
    main()
