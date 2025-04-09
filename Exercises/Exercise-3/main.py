import boto3
import requests
import gzip
import shutil
import pandas as pd
import os

path = "/Users/william/Documents/data-engineering-practice/Exercises/Exercise-3/downloads"
url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2022-05/wet.paths.gz'
base_url = 'https://data.commoncrawl.org/'
file = 'wet.paths.gz'

def download_extract_files(url,file):

    try:
        uri = requests.get(url)
        with open(path+'/'+file,'wb') as f:
            f.write(uri.content)
            print(f"{f} baixado com sucesso")
    except requests.RequestException as e:
        return f"erro ao baixar arquivo {e}"
    
    with gzip.open(path+'/'+file,'rb' ) as gz_in:
       with open(path+'/'+file+'_out', 'wb') as gz_out:
           shutil.copyfileobj(gz_in, gz_out)
           out = gz_out


def main():

    #try:
    #    uri = requests.get(url)
    #    with open(path+'/'+file,'wb') as f:
    #        f.write(uri.content)
    #        print(f"{f} baixado com sucesso")
    #except requests.RequestException as e:
    #    return f"erro ao baixar arquivo {e}"

    #with gzip.open(path+'/'+file,'rb' ) as gz_in:
    #   with open(path+'/'+file+'_out', 'wb') as gz_out:
    #       shutil.copyfileobj(gz_in, gz_out)
    #       out = gz_out

    download_extract_files(url,file)
    
    file_out = (file+'_out')
    
    with open(path+'/'+file_out, 'r') as fo:
            first_row = fo.readline()
    
    url_2 = (base_url + first_row).strip()
    file_2 = os.path.basename(url_2)
    print(file_2)

    download_extract_files(url_2,file_2)

    #try:
    #    uri_last = requests.get(uri_2)
    
    #    with open(path+'/'+file_2,'wb') as f:
    #        f.write(uri_last.content)
    #        print(f"{f} baixado com sucesso")
    #except requests.RequestException as e:
    #    return f"erro ao baixar arquivo {e}"
    
    #with gzip.open(path+'/'+file_2,'rb' ) as gz_in:
    #   with open(path+'/'+file_2+'_out', 'wb') as gz_out:
    #       shutil.copyfileobj(gz_in, gz_out)
           
    pass
if __name__ == "__main__":
    main()
