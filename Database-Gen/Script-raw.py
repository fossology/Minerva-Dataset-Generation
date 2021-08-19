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

import ast
import os
import string
import re
import glob
import random
from pathlib import Path
import pandas as pd
from collections import defaultdict
from typing import List
import intxeger
import multiprocessing
import time
import itertools
import numpy as np


def main(dictionary,spdxregex,ltregex):
    for key in dictionary:
        if dictionary[key]=="":
            continue
        
        content = dictionary[key]
        
        para = sum(line.isspace() for line in content) + 1
        contents = content.split('\n\n')
        text = ". ".join(contents)
        text = clean_license(text)
        reg1 = spdxregex.loc[spdxregex['Licenses'].str.contains(key.split('-').pop(0)),'Regex'].values.tolist()
        reg2 = ltregex.loc[ltregex['Licenses'].str.contains(key.split('-').pop(0)),'Regex'].values.tolist()
        ab = itertools.chain(reg1,reg2)
        regex = list(ab)
        regex_list = []
        rep = {"=FEW=": ".{1,32}", "=SOME=": ".{1,60}", "=ANY=": ".{1,60}"} 
        rep = dict((re.escape(k), v) for k, v in rep.items()) 
        pattern = re.compile("|".join(rep.keys()))
        for r in regex:
            r = pattern.sub(lambda m: rep[re.escape(m.group(0))], r)
            regex_list.append(r)

        regex_list = list(filter(None, regex_list))

        if len(regex_list)==0:
            continue
        for reg in regex_list:
            reg = reg.strip().replace('"', '')
            expansion = []
            if "(.{1,32} (AND|OR)){1,4}" in reg:
                prevsen = reg.split("(.{1,32} (AND|OR)){1,4}")[0]
                latersen = reg.split("(.{1,32} (AND|OR)){1,4}")[-1]  
                for i in range(2,8):
                    m = create_ngram_model(i,key)
                    for i in range(1,len(text)):
                        random.seed(i)
                        generated_text = m.generate_text(np.random.randint(6,32))
                        generated_text = clean_license(generated_text)
                        generated_text = generated_text.lower()
                        expansion.append(generated_text)
                        expansion = list(set(expansion))
                expansion_ = regex_expansion(prevsen,expansion,latersen)
            elif ".{1,32}" in reg:
                prevsen = reg.split(".{1,32}")[0]
                latersen = reg.split(".{1,32}")[-1]
                for i in range(2,8):
                    m = create_ngram_model(i,text)
                    for i in range(1,len(text)):
                        random.seed(i)
                        generated_text = m.generate_text(np.random.randint(6,32))
                        generated_text = clean_license(generated_text)
                        generated_text = generated_text.lower()
                        expansion.append(generated_text)
                        expansion = list(set(expansion))
                expansion_ = regex_expansion(prevsen,expansion,latersen)
            elif ".{1,60}" in reg:
                prevsen = reg.split("(.{1,60}")[0]
                latersen = reg.split("(.{1,60}")[-1]
                for i in range(2,8):
                    m = create_ngram_model(i,text)
                    for i in range(1,len(text)):
                        random.seed(i)
                        generated_text = m.generate_text(np.random.randint(12,60))
                        generated_text = clean_license(generated_text)
                        generated_text = generated_text.lower()
                        expansion.append(generated_text)
                        expansion = list(set(expansion))
                expansion_ = regex_expansion(prevsen,expansion,latersen)
            else:
                expansion_ = []
                expansion_ = licensestatement_(reg)
            
            filegen = 0
            for i in range(para):
                try:
                    part = str(contents[i])
                    for ind in range(len(expansion_)):
                        filegen+=1                            
                        with open('{}-{}.txt'.format(key,filegen), 'w') as o1:
                            o1.write(part+" "+expansion_[ind])
                except:
                    break
                
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

def regex_expansion(prevsen,input_list,latersen):
    res_=[]
    while(len(res_)<200):
        final_regex = ""
        num = random.randint(1,4)
        for i in range(num):
            final_regex = final_regex + np.random.choice(input_list)+" (and|or) "
            fregex_ = prevsen + " " + final_regex + " " + latersen
            ans = licensestatement_(fregex_)
        for i in ans:
            i = re.sub("[\s]+", " ",i)
            res_.append(i)
    return res_

def generate_statements():
    for i in range(2,20):
      m = create_ngram_model(i,text)
      
      for i in range(1,len(text)):
        random.seed(i)
        generated_text = m.generate_text(np.random.randint(6,31))
        generated_text = clean_license(generated_text)
        generated_text = generated_text.lower()
        expansion.append(generated_text)
        expansion = list(set(expansion))

def tokenize(text: str) -> List[str]:
    for punct in string.punctuation:
        text = text.replace(punct, ' '+punct+' ')
    t = text.split()
    return t

def get_ngrams(n: int, tokens: list) -> list:
    tokens = (n-1)*['<START>']+tokens
    l = [(tuple([tokens[i-p-1] for p in reversed(range(n-1))]), tokens[i]) for i in range(n-1, len(tokens))]
    return l


class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.context = {}
        self.ngram_counter = {}

    def update(self, sentence: str) -> None:
        n = self.n
        ngrams = get_ngrams(n, tokenize(sentence))
        for ngram in ngrams:
            if ngram in self.ngram_counter:
                self.ngram_counter[ngram] += 1.0
            else:
                self.ngram_counter[ngram] = 1.0

            prev_words, target_word = ngram
            if prev_words in self.context:
                self.context[prev_words].append(target_word)
            else:
                self.context[prev_words] = [target_word]

    def prob(self, context, token):
        try:
            count_of_token = self.ngram_counter[(context, token)]
            count_of_context = float(len(self.context[context]))
            result = count_of_token / count_of_context

        except KeyError:
            result = 0.0
        return result

    def random_token(self, context):
        r = random.random()
        map_to_probs = {}
        token_of_interest = self.context[context]
        for token in token_of_interest:
            map_to_probs[token] = self.prob(context, token)

        summ = 0
        for token in sorted(map_to_probs):
            summ += map_to_probs[token]
            if summ > r:
                return token

    def generate_text(self, token_count: int):
        n = self.n
        context_queue = (n - 1) * ['<START>']
        result = []
        for _ in range(token_count):
            obj = self.random_token(tuple(context_queue))
            result.append(obj)
            if n > 1:
                context_queue.pop(0)
                if obj == '.':
                    context_queue = (n - 1) * ['<START>']
                else:
                    context_queue.append(obj)
        return ' '.join(result)


def create_ngram_model(n, text):
    m = NgramModel(n)
    for sentence in text:
        sentence += '.'
        m.update(sentence)
    return m

if __name__ == "__main__":
    with open("database_licenses.txt", "r") as data:
        dictionary = ast.literal_eval(data.read())

    spdxregex = pd.read_csv("STRINGSin-Regex-Extraction\SPDXRegex.csv")
    ltregex = pd.read_csv("STRINGSin-Regex-Extraction\LTRegex.csv")
    res1 = dict(list(dictionary.items())[:len(dictionary)//3])
    res2 = dict(list(dictionary.items())[len(dictionary)//3:(2*len(dictionary)//3)])
    res3 = dict(list(dictionary.items())[(2*len(dictionary)//3):])

    list_data = [(res1,spdxregex,ltregex),(res2,spdxregex,ltregex),(res3,spdxregex,ltregex)]

    with multiprocessing.Pool(processes=3) as pool:
        pool.starmap(main,list_data)