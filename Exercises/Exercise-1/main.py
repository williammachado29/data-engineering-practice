import requests
import os
from zipfile import ZipFile , is_zipfile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

path = "/app/downloads"


def main():
    # your code here
    if not os.path.exists(path):
     os.mkdir(path)
     print("Folder %s created!" % path)
    else:
     print("Folder %s already exists" % path)

    for i in download_uris:
        response = requests.get(i)
        path_filename = os.path.join(path,os.path.basename(response.url))
        
        with open(path_filename,'wb') as file:
            file.write(response.content)
        if is_zipfile(path_filename) == True:
            with ZipFile(path_filename,'r') as file_z:
                file_z.extractall(path=path)
                print(f'{path_filename} extracted succesfully')
        else:
            print(f'{path_filename} not a Zip File')
        os.remove(str(path_filename))
            
pass

if __name__ == "__main__":
    main()
