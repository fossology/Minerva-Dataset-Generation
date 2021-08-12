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

import intxeger
import os
import requests
import string
import re
import random
from pathlib import Path
import pandas as pd
from collections import defaultdict
import multiprocessing
import time 

def clean_license(text):
  license = text
  license = re.sub(r'\w*\d\w*', '', license)
  license = re.sub("[\n]+", "\n",license)
  license = license.strip()
  punctuationNoPeriod = "[" + "(" + ")" + "]"
  license = re.sub(punctuationNoPeriod, "", license)
  license = license.translate(str.maketrans('', '', string.punctuation))
  license =  re.sub(r"\b[a-zA-Z]\b", "", license)
  license = re.sub("[\s]+", " ",license)
  license = license.replace('"', '')  
  return license

def regex_expansion(prevsen,latersen,text):
  result = []
  while(len(result)<100):
    final_regex = ""
    num = random.randint(1,4)
    for i in range(num):
      final_regex = final_regex + generate_sen(markov_chain(text),random.randint(1,32),text)+" "
    fregex_ = prevsen + final_regex + latersen
    ans = licensestatement_(fregex_)
    for i in ans:
      i = re.sub("[\s]+", " ",i)
      if i not in result:
        result.append(i)
  return result

def generate_sen(chain, count, text):
  text = re.sub(r'\w*\d\w*', '', text)
  words = text.split(' ')
  words = [word.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) for word in words]
  words = [word.lower() for word in words]
  word1 = random.choice(words)
  sentence = word1
  for i in range(count-2):
    try:
      word2 = random.choice(chain[word1])
      word1 = word2
      sentence += ' ' + word2
    except:
      continue
  return sentence

def markov_chain(text):
  words = text.split(' ')
  words = [word.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) for word in words]
  words = [word.lower() for word in words]
  m_dict = defaultdict(list)
  for current_word, next_word in zip(words[0:-1], words[1:]):
      current_word = re.sub(r'\w*\d\w*', '', current_word)
      m_dict[current_word].append(next_word)
  m_dict = dict(m_dict)
  return m_dict

def licensestatement_(regex_):
  x = intxeger.build(regex_)
  res=x.sample(N=1)
  result = res
  i=2
  while True:
      try:
        result = res
        result = list(set(result))
        if len(result) >10:
          return result 
        res = x.sample(N=i)
        i+=1
      except:    
        break
  return result

def main(data,spdxregex):
    count = 1
    for key in data:
        count+=1
        with open(key, 'r') as f:
            para = sum(line.isspace() for line in f) + 1
        content = data[key]
        basefile = os.path.basename(key).split(".")[0]
        print("For file : ",basefile)

        contents = content.split('\n\n')
        text = ". ".join(contents)
        text = clean_license(text)
        for i in range(para):
            try: 
                with open(os.path.join('C:/Users/Documents/GSOC21/markov-dataset','{}-{}.txt'.format(basefile,i+1)), 'w') as o1:
                    o1.write(str(contents[i]))
                filegen = i
            except:
                break
        reg = spdxregex.loc[spdxregex['Licenses']==basefile]
        if reg.empty:
            continue
        reg = reg.values[0][1].strip().replace('"', '')
        prevsen = reg.split("(.{1,32} (AND|OR)){1,4}")[0]
        latersen = reg.split("(.{1,32} (AND|OR)){1,4}")[-1]
        expansion = []
        expansion = regex_expansion(prevsen,latersen,text)
        for i in range(para):
            try:
                part = str(contents[i])
                for ind in range(len(expansion)):
                    filegen += 1
                    with open(os.path.join('C:/Users/Documents/GSOC21/markov-dataset','{}-{}.txt'.format(basefile,filegen)), 'w') as o1:
                        o1.write(part+" "+expansion[ind])
            except:
                break
    return count

if __name__ == "__main__":
    start = time.time()
    data = {}
    for root, dirs, files in os.walk("C:/Users/Documents/GSOC21/SPDX-Dataset"):
        for file_ in files:
            filepath = os.path.join(root,file_)
            with open(filepath,"r",encoding="utf8") as f:
                content = f.read()
                data[filepath] = content

    spdxregex = pd.read_csv("C:/Users/Documents/Downloads/SPDX_regex.csv")

    res1 = dict(list(data.items())[:len(data)//3])
    res2 = dict(list(data.items())[len(data)//3:(2*len(data)//3)])
    res3 = dict(list(data.items())[(2*len(data)//3):])

    list_data = [(res1,spdxregex),(res2,spdxregex),(res3,spdxregex)]

    with multiprocessing.Pool(processes=3) as pool:
        num = pool.starmap(main,list_data)
    
    print("Total licenses scanned : ",num)
    
    end = time.time()

    print("Time Taken = ", end-start)