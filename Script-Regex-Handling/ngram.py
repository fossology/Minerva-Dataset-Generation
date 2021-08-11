import os
import requests
import string
import re
import glob
import random
from pathlib import Path
import pandas as pd
import json
from collections import defaultdict
from typing import List
import intxeger
import numpy as np
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
      final_regex = final_regex + np.random.choice(input_list)+" (AND|OR) "
    fregex_ = prevsen + " " + final_regex + " " + latersen
    ans = licensestatement_(fregex_)
    for i in ans:
      i = re.sub("[\s]+", " ",i)
      res_.append(i)
  return res_

def generate_statements():
    for i in range(2,20):
      m = create_ngram_model(i,key)
      
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


def create_ngram_model(n, path):
    m = NgramModel(n)
    with open(path, 'r') as f:
        text = f.read()
        text = text.split('.')
        for sentence in text:
            # add back the fullstop
            sentence += '.'
            m.update(sentence)
    return m

def main(data,spdxregex,errorlist):
    print("Starting this function")
    for key in data:
        with open(key, 'r',encoding="utf8") as f:
            para = sum(line.isspace() for line in f) + 1
        content = data[key]
        basefile = os.path.basename(key).split(".")[0]
        contents = content.split('\n\n')
        text = ". ".join(contents)
        text = clean_license(text)
        reg = spdxregex.loc[spdxregex['Licenses']==basefile]
        if reg.empty:
            errorlist.append(key)
            continue
        reg = reg.values[0][1].strip().replace('"', '')
        prevsen = reg.split("(.{1,32} (AND|OR)){1,4}")[0]
        latersen = reg.split("(.{1,32} (AND|OR)){1,4}")[-1]
        
        expansion = []
        for i in range(2,8):
            m = create_ngram_model(i,key)
            for i in range(1,len(text)):
                random.seed(i)
                generated_text = m.generate_text(np.random.randint(6,31))
                generated_text = clean_license(generated_text)
                generated_text = generated_text.lower()
                expansion.append(generated_text)
                expansion = list(set(expansion))
        filegen = 0
        expansion_ = []
        expansion_ = regex_expansion(prevsen,expansion,latersen)
        for i in range(para):
            try:
                part = str(contents[i])
                for ind in range(len(expansion_)):
                    filegen += 1
                    with open(os.path.join('C:/Users/Documents/GSOC21/test','{}-{}.txt'.format(basefile,filegen)), 'w') as o1:
                        o1.write(part+" "+expansion_[ind])
            except:
                break
    
    return errorlist
    

if __name__ == "__main__":
    start = time.time()
    data = {}
    for root, dirs, files in os.walk("C:/Users/Documents/GSOC21/SPDX-Dataset"):
        for file_ in files:
            filepath = os.path.join(root,file_)
            with open(filepath,"r",encoding="utf8") as f:
                content = f.read()
                # basefile = os.path.basename(filepath).split(".")[0]
                data[filepath] = content

    spdxregex = pd.read_csv("C:/Users/Documents/Downloads/SPDX_regex.csv")

    res1 = dict(list(data.items())[:len(data)//3])
    res2 = dict(list(data.items())[len(data)//3:(2*len(data)//3)])
    res3 = dict(list(data.items())[(2*len(data)//3):])

    errorlist1 = []
    errorlist2 = []
    errorlist3 = []

    list_data = [(res1,spdxregex,errorlist1),(res2,spdxregex,errorlist2),(res3,spdxregex,errorlist3)]

    with multiprocessing.Pool(processes=3) as pool:
        results = pool.starmap(main,list_data)
    
    df = pd.DataFrame(results)
    df.to_csv('errorlistoffiles.csv',index = False)
    
    end = time.time()

    print("Time Taken = ", end-start)