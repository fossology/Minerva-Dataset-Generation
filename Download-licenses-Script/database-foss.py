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


def main():
    download = "..\\Original-DB-Foss-Dataset"
    os.makedirs(download, exist_ok=True)
    url = 'https://raw.githubusercontent.com/fossology/fossology/master/install/db/licenseRef.json'
    response = urlopen(url)
    data_json = json.loads(response.read())
    for licenses in data_json:
        with open(download+'\\'+licenses["rf_shortname"], 'w', encoding='utf-8') as o1:
            o1.write(licenses["rf_text"])


if __name__ == "__main__":
    main()
