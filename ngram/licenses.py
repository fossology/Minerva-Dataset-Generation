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
from .preprocessing import *
from .regex_handling import *
from .ngram import *
import argparse
import pandas as pd
import random
import pathlib
import multiprocessing
import numpy as np


def chunkIt(seq, num):
    return np.array_split(seq, num)


def read_directory(path):
    barlist = list()
    for root, dirs, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1].lower() == ".txt":
                barlist.append(os.path.join(root, f))
    return barlist


def file_vocab(filename):
    vfile = os.path.join("../Original-SPDX-Dataset", filename + '.txt')
    with open(vfile, 'r', encoding='unicode_escape') as f:
        vocab = f.read()
    return vocab


def file_regex(filepath, regexcsv):
    licensename = os.path.sep.join(filepath.split(
        os.path.sep)[0:-1]).split(os.path.sep)[-1]
    df = pd.read_csv(regexcsv)
    var = df.loc[df.Licenses == licensename, 'Regex']
    if var.shape[0] == 0:
        return ""
    else:
        return var.values[0]


def main(files, regexcsv):

    pathlib.Path("ngramfiles").mkdir(parents=True, exist_ok=True)

    for file in files:
        filename = os.path.sep.join(file.split(os.path.sep)[
                                    0:-1]).split(os.path.sep)[-1]
        with open(file, 'r', encoding='unicode_escape') as f:
            content = f.read()
        vocabulary = file_vocab(filename)
        regex = file_regex(file, regexcsv)
        regex = regex.strip().replace('"', '')

        if len(regex) == 0:
            continue
        os.makedirs(os.path.join("ngramfiles", filename), exist_ok=True)
        preregex = regex.split("(.{1,32} (AND|OR)){1,4}")[0]
        secregex = regex.split("(.{1,32} (AND|OR)){1,4}")[-1]

        expansion = []
        for ind in range(2, 8):
            m = create_ngram_model(ind, file)
            for i in range(1, len(vocabulary)):
                random.seed(i)
                generated_text = m.generate_text(np.random.randint(6, 31))
                generated_text = preprocessing_text(generated_text).lower()
                expansion.append(generated_text)
                expansion = list(set(expansion))

        expansion_regex = regex_expansion(preregex, expansion, secregex)
        lst = os.listdir(os.path.join("ngramfiles", filename))
        count = len(lst)

        for ind in range(len(expansion_regex)):
            count += 1
            with open(os.path.join(
                    os.path.join("ngramfiles", filename),
                    f"""{filename}-{count}.txt"""),
                    'w', encoding='unicode_escape') as o1:

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

    try:
        inputpath = args.inputpath
        if not os.path.isdir(inputpath):
            raise TypeError
    except TypeError:
        print("Valid License directory not provided")

    try:
        regexcsv = args.regexcsv
        if not os.path.isfile(regexcsv):
            raise TypeError
        if os.path.splitext(regexcsv)[1].lower() != ".csv":
            raise TypeError
    except TypeError:
        print("Invalid File or path provided. Expected csv filepath")

    try:
        n = int(args.cores)
        if n <= 0:
            raise ValueError
    except ValueError:
        print("Number of cores cannot be a string, zero or a negative number")

    samples = read_directory(inputpath)
    ls = chunkIt(samples, n)
    list_data = [(ls[i], regexcsv) for i in range(len(ls))]

    with multiprocessing.Pool(processes=n) as pool:
        pool.starmap(main, list_data)
