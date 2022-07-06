from gettext import install

import os, re

import time
import requests
import jsonpath


def get_valid_title(filename):
    '''
    #get file name
    #param filename:
    #return:
    '''
    rstr = r"[\/\\\:：\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    filename = re.sub(rstr, "_", filename)
    filename = re.sub('_+', '_', filename)
    return filename


def main(pro_id):
    base_url = 'https://zap-api-production.herokuapp.com/document/package'
    url = f'https://zap-api-production.herokuapp.com/projects/{pro_id}?include=actions,milestones,dispositions,dispositions.action,users,assignments.user,packages,artifacts'
    headers = {
        "Host": "zap-api-production.herokuapp.com",
        "Origin": "https://zap.planning.nyc.gov",
        "Pragma": "no-cache",
        "Referer": "https://zap.planning.nyc.gov/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    # print(res.text)
    serverRelativeUrls = jsonpath.jsonpath(res.json(), '$..serverRelativeUrl')
    print(len(serverRelativeUrls))
    for serverRelativeUrl in serverRelativeUrls:
        url = base_url + serverRelativeUrl  #pdf link

        title = get_valid_title(url.split('/')[-1].replace('.pdf', '').replace('.PDF', '')) + '.pdf'
        if title in os.listdir():
            print(title + "existed")
            continue
        res = requests.get(url, headers=headers)
        with open(f'{dir_name}/{pro_id}/{title}', 'wb') as f:
            f.write(res.content)
        print(url + 'download finished')


def get_ids():
    url = 'https://zap-api-production.herokuapp.com/projects?dcp_publicstatus%5B%5D=In%20Public%20Review&dcp_publicstatus%5B%5D=Noticed&page=1'
    res = requests.get(url)
    dic = res.json()
    ids = jsonpath.jsonpath(dic, '$..id')
    return ids


if __name__ == '__main__':
    dir_name = 'result'
    os.makedirs(dir_name, exist_ok=True)
    ids = get_ids()
    for pro_id in ids:
        origin_url = f'https://zap.planning.nyc.gov/projects/{pro_id}'
        if pro_id not in os.listdir(dir_name):
            os.makedirs(f'result/{pro_id}', exist_ok=True)
        main(pro_id)
        time.sleep(2)
