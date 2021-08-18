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

def extract_spdx():
  """
  There are 460 files of SPDX licenses in licenseListVersion: 3.13
  url of latest SPDX Exception release = https://spdx.org/licenses/licenses.json
  """  
  download = "..\\Original-SPDX-Dataset"
  os.makedirs(download, exist_ok=True)
  url = 'https://spdx.org/licenses/licenses.json'
  response = urlopen(url)
  data_json = json.loads(response.read())

  for license in data_json["licenses"]:
    url2 = 'https://spdx.org/licenses/licenses.json'
    response2 = urlopen(url2)
    data_json2 = json.loads(response2.read())

    with open(download+'\\'+license["licenseId"], 'w', encoding='utf-8') as o1:
          o1.write(data_json2["licenseText"])

if __name__ == "__main__":
    extract_spdx()