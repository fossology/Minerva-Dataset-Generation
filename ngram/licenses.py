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
import os
from os import walk
from os.path import splitext
from os.path import join
from preprocessing import *
from regex_handling import *
from ngram import *
import argparse
import pandas as pd
import random
import pathlib
import multiprocessing

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def read_directory(path):
    barlist = list()
    for root, dirs, files in os.walk(path):
      for f in files:
        if splitext(f)[1].lower() == ".txt":
          barlist.append(os.path.join(root, f))
    #print(barlist)
    return barlist

def file_vocab(filename):
    vfile = os.path.join("../Original-SPDX-Dataset",filename + '.txt')
    # licensename = filepath.split('\\')[-1]
    with open(vfile, 'r', encoding = 'unicode_escape') as f:
        vocab = f.read()
    return vocab

def file_regex(filepath, regexcsv):
    licensename = os.path.sep.join(filepath.split(os.path.sep)[0:-1]).split(os.path.sep)[-1]
    df = pd.read_csv(regexcsv)
    var = df.loc[df.Licenses==licensename,'Regex']
    if var.shape[0] == 0:
        return ""
    else:
        return var.values[0]

def main(files, regexcsv):

    pathlib.Path("ngramfiles").mkdir(parents=True, exist_ok=True)
    # files = read_directory(path)
    
    for file in files:
        filename = os.path.sep.join(file.split(os.path.sep)[0:-1]).split(os.path.sep)[-1]
        with open(file, 'r', encoding = 'unicode_escape') as f:
            content = f.read()
        vocabulary = file_vocab(filename)
        regex = file_regex(file, regexcsv)
        regex = regex.strip().replace('"', '')

        if len(regex)==0:
            # print('Regex not found for -> ', filename)
            continue
        os.makedirs(os.path.join("ngramfiles",filename), exist_ok=True)
        preregex = regex.split("(.{1,32} (AND|OR)){1,4}")[0]
        secregex = regex.split("(.{1,32} (AND|OR)){1,4}")[-1]

        expansion = []
        for ind in range(2,8):
            m = create_ngram_model(ind,file)
            for i in range(1,len(vocabulary)):
                random.seed(i)
                generated_text = m.generate_text(np.random.randint(6,31))
                generated_text = preprocessing_text(generated_text).lower()
                expansion.append(generated_text)
                expansion = list(set(expansion))

        expansion_regex = regex_expansion(preregex,expansion,secregex)
        lst = os.listdir(os.path.join("ngramfiles",filename))
        count = len(lst)

        for ind in range(len(expansion_regex)):
            count+=1
            with open(os.path.join(os.path.join("ngramfiles",filename),'{}-{}.txt'.format(filename,count)), 'w', encoding = 'unicode_escape') as o1:
                o1.write(content + '.' + expansion_regex[ind])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputpath",
        default="..\\Split-SPDX-licenses",
        help="Specify the input file/directory path",
    )
    parser.add_argument(
        "--regexcsv",
        default="..\\STRINGSin-Regex-Extraction\\SPDXRegex.csv",
        help="Specify the input regex csv path",
    )

    parser.add_argument(
        "--cores",
        default=1,
        help="Specify the number of core(s)",
    )

    args = parser.parse_args()
    inputpath = args.inputpath
    regexcsv = args.regexcsv
    n = int(args.cores)

    samples = read_directory(inputpath)
    ls = chunkIt(samples, n)
    list_data = []

    for i in range(len(ls)):
        list_data.append((ls[i], regexcsv))

    with multiprocessing.Pool(processes=n) as pool:
        pool.starmap(main, list_data)

    # main(inputpath, regexcsv)

