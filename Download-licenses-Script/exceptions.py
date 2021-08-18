"""
 Copyright (C) 2021 Shreya Singh (shreya.out@gmail.com)

 SPDX-License-Identifier: GPL-2.0

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License along
 with this program; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from urllib.request import urlopen
import json
import os

def extract_exceptions():
  """
  There are 41 files of SPDX exception in licenseListVersion: 3.13
  url of latest SPDX Exception release = https://spdx.org/licenses/exceptions.json
  """
  download = "..\\Original-SPDX-Dataset"
  os.makedirs(download, exist_ok=True)
  url = 'https://spdx.org/licenses/exceptions.json'
  response = urlopen(url)
  data_json = json.loads(response.read())

  for license in data_json["exceptions"]:
    license["reference"] = license["reference"].replace("./","https://spdx.org/licenses/",1)
    url2 = license["reference"]
    response2 = urlopen(url2)
    data_json2 = json.loads(response2.read())
    
    with open(download+'\\'+license["licenseExceptionId"], 'w') as o1:
          o1.write(data_json2["licenseExceptionText"])

if __name__ == "__main__":
    extract_exceptions()