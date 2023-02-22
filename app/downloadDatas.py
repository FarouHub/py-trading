import requests
import zipfile
from bs4 import BeautifulSoup


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open('../datas/' + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename


# téléchargement des zip des données binance pour une pair donnée
def downloadData():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    url = "https://data.binance.vision/?prefix=data/futures/um/daily/klines/BTCUSDT/5m/"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    
    for link in soup.find_all("a").get('href'):
        if link.endswith('.zip'):
            # on télécharge
            fileName = download_file(link)
            # on dézip
            with zipfile.ZipFile('../datas/'+ fileName, 'r') as zip_ref:
                zip_ref.extractall('../datas/')

def cleanning():
    # on mouve les fichiers et on supprime les fichiers .zip
    print('ok')


