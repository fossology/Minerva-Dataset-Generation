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

import re
from pathlib import Path
import pandas as pd

def extract(content):
  content = re.split("[#]+",content)
  result = []
  for text in content:
    if text.lstrip().startswith('%'):
      text = text.split('\n\n')
      for j in text:
        j = j.replace("\n"," ")
        result.append(j)
  org = []
  regex = []
  for i in range(len(result)):
    regex.append(result[i].split("%STR%",1)[1])
    tokens = re.findall("[\w']+", result[i])
    org.append(tokens[1])
    sen = result[i].split("%STR%",1)[0]
  df = pd.DataFrame({'License':org,'Regex':regex})
  df['License'] = df['License'].apply(lambda x: x.replace("_LT_",""))
  df.to_csv('LTRegex.csv',index=False)

if __name__ == "__main__":
  content = Path("/STRINGS.in-Regex-Extraction/license_regex.txt").read_text() 
  extract(content)