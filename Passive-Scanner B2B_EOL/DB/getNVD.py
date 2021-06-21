
import re
import io



import os, json, csv
from bs4 import BeautifulSoup
import requests, zipfile
from io import StringIO

def download(url_path):
    print('[*] Download NVT: ' + url_path.split('/')[-1])
    request = requests.get('https://nvd.nist.gov' + url_path)
    # save
    output = open(url_path.split('/')[-1], "wb")
    output.write(request.content)
    output.close()

def get_urls():

    response = requests.get('https://nvd.nist.gov/vuln/data-feeds')

    soup = BeautifulSoup(response.text, "html.parser" )
    links = soup.find_all('a')

    for tag in links:
        link = tag.get('href', None)
        if (link is not None) and ('.json.zip' in link):
            download(link)

def list_files():
    CurrentPath = os.getcwd()
    files = []
    for r, d, f in os.walk(CurrentPath):
        for file in f:
            if '.json.zip' in file.lower():
                files.append(os.path.join(r, file))
    return files


def parse_json(file):
    print('[*] Processing file: ' + file.split('\\')[-1])
    archive = zipfile.ZipFile(file, 'r')
    jsonfile = archive.open(archive.namelist()[0])
    cve_dict = json.loads(jsonfile.read())
    jsonfile.close()

    f = open("nvd.csv", "a+")

    try:
        for entry in cve_dict['CVE_Items']:

            CVE = str(entry['cve']['CVE_data_meta']['ID'])
            BY = str(entry['cve']['CVE_data_meta']['ASSIGNER'])
            DESCRIPTION = str(entry['cve']['description']['description_data'][0]['value'])
            try:
                SEVERITY = str(entry['impact']['baseMetricV2']['severity'])
            except:
                SEVERITY = str('unknown')


            f.write(CVE + ',' + DESCRIPTION+ ',' + SEVERITY+ ',' + BY + '\n')
        f.close()
    except Exception as err:
        print('[!] Error in processing file ' + file.split('\\')[-1] + " " + str(err))






get_urls()

for file in list_files():
    parse_json(file)
    os.remove(file)

print('[*] NVD Database Generated!')