import requests
import pandas as pd
import json
import re
import os

def extract_exceptions():
  """
  There are 41 files of SPDX exception in licenseListVersion: 3.13
  url of latest SPDX Exception release = https://spdx.org/licenses/exceptions.json
  """
  r = requests.get(url='https://spdx.org/licenses/exceptions.json')
  data = r.json()

  for license in data["exceptions"]:
    license["reference"] = license["reference"].replace("./","https://spdx.org/licenses/",1)
    license_text = requests.get(url=license["reference"])
    license_dict = license_text.json()
    
    with open(os.path.join('{}.txt'.format(license["licenseExceptionId"])), 'w') as o1:
          o1.write(license_dict["licenseExceptionText"])

if __name__ == "__main__":
    extract_exceptions()