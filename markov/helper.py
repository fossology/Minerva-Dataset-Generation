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
import pandas as pd
import re
import string


def preprocessing_text(text):
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub("[\n]+", "\n", text)
    text = text.strip()
    punctuationNoPeriod = "[" + "(" + ")" + "]"
    text = re.sub(punctuationNoPeriod, "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r"\b[a-zA-Z]\b", "", text)
    text = re.sub("[\s]+", " ", text)
    text = text.replace('"', '')
    return text


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
