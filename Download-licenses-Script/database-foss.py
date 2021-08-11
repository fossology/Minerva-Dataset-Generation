import requests
import json
import os

def main():
    r = requests.get(url='https://raw.githubusercontent.com/fossology/fossology/master/install/db/licenseRef.json')
    data = r.json()
    for licenses in data:
        with open(os.path.join('D:/Projects/SPDX/Fossology-Database','{}.txt'.format(licenses["rf_shortname"])), 'w', encoding ='utf-8') as o1:
                o1.write(licenses["rf_text"])
    
if __name__ == "__main__":
    main()
