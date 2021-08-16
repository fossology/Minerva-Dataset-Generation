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

import requests
import json
import os

def extract_spdx():
  """
  There are 460 files of SPDX licenses in licenseListVersion: 3.13
  url of latest SPDX Exception release = https://spdx.org/licenses/licenses.json
  """  
  download = "..\\Original-SPDX-Dataset"
  os.makedirs(download, exist_ok=True)
  r = requests.get(url='https://spdx.org/licenses/licenses.json')
  data = r.json()
  for license in data["licenses"]:
    print(license["licenseId"])
    license_text = requests.get(url=license["detailsUrl"])
    license_dict = license_text.json()

    with open(download+'\\'+license["licenseId"], 'w', encoding='utf-8') as o1:
          o1.write(license_dict["licenseText"])

if __name__ == "__main__":
    extract_spdx()