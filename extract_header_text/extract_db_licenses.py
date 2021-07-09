import requests
import ndjson 
import json
import pandas as pd

def db_licenses():
    database_licenses = {}
    response = requests.get("https://raw.githubusercontent.com/fossology/fossology/master/install/db/licenseRef.json")
    items = response.json()
    num_of_license = 0
    for lic in items:
        num_of_license += 1
        print("For license : ",lic["rf_fullname"])
        if lic["rf_text"] != '':
            database_licenses[lic["rf_shortname"]] = lic["rf_text"]
        print("======================================")
    with open('database_licenses.txt', 'w') as convert_file:
        convert_file.write(json.dumps(database_licenses))
    return num_of_license

if __name__ == "__main__":
    num = db_licenses()
    print("Number of total licenses extracted : ", num)
