import requests
import json
import os

def extract_spdx():
  """
  There are 460 files of SPDX licenses in licenseListVersion: 3.13
  url of latest SPDX Exception release = https://spdx.org/licenses/licenses.json
  """  
  r = requests.get(url='https://spdx.org/licenses/licenses.json')
  data = r.json()
  for license in data["licenses"]:
    print(license["licenseId"])
    license_text = requests.get(url=license["detailsUrl"])
    license_dict = license_text.json()

    with open(os.path.join('{}.txt'.format(license["licenseId"])), 'w', encoding='utf-8') as o1:
          o1.write(license_dict["licenseText"])

if __name__ == "__main__":
    extract_spdx()