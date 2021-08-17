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
import pandas as pd

def read_directory(path):
    barlist = list()
    for root, dirs, files in os.walk(path):
      for f in files:
        if splitext(f)[1].lower() == ".txt":
          barlist.append(os.path.join(root, f))
    #print(barlist)
    return barlist

def file_vocab(filename):
    vfile = "..\\Original-SPDX-Dataset\\" + filename + '.txt'
    # licensename = filepath.split('\\')[-1]
    with open(vfile, 'r', encoding = 'unicode_escape') as f:
        vocab = f.read()
    return vocab

def file_regex(filepath, regexcsv):
    licensename = '\\'.join(filepath.split('\\')[0:-1]).split('\\')[-1]
    df = pd.read_csv(regexcsv)
    var = df.loc[df.Licenses==licensename,'Regex']
    if var.shape[0] == 0:
        return ""
    else:
        return var.values[0]