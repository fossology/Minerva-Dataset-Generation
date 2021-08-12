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
import os
import argparse

def splitter(file,dirname):
    
    history = []
    with open(file, 'r', encoding= 'unicode_escape') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    text = " ".join(content)
    content = text.split(". ")
    content = [x.strip() for x in content]
    para = ""
    for comb  in range(1,len(content)):
        for i in range(0, len(content)-comb+1, comb):
            if len(history)>1000:
                history = list(set(history))
                if len(history)>1000:
                    break
            para = para  + " " +  content[i]
            para = re.sub("\s\s+" , " ", para)
            para = para.strip()
            if para not in history:
                history.append(para)
    history = list(set(history))
    generate_files(file,history,dirname)

                
def generate_files(file,history,dirname):
    counter = 0
    os.makedirs(dirname, exist_ok=True)
    for texts in history:
        counter+=1
        name = dirname + '-{}.txt'.format(counter)
        with open(os.path.join(dirname,name), 'w', encoding= 'unicode_escape') as o1:
                    o1.write(texts)
    naive_approach(file,dirname,counter)

def naive_approach(file,dirname,counter):
    os.makedirs(dirname, exist_ok=True)

    with open(file, 'r', encoding= 'unicode_escape') as f:
        para = sum(line.isspace() for line in f) + 1

    with open(file, 'r+', encoding= 'unicode_escape') as f:
        contents = f.read()

    content = contents.split('\n\n')

    for i in range(para):
        counter += 1
        name = dirname + '-{}.txt'.format(counter)
        try:
            with open(os.path.join(dirname,name), 'w', encoding= 'unicode_escape') as o1:
                o1.write(str(content[i]))
        except:
            break

def main(path):
    for roots, dirs, files in os.walk(path,topdown=True):
        for name in files:
            dirname = os.path.splitext(name)[0]
            file = os.path.join(path,name)
            splitter(file,dirname)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Pass a directory to find original licenses')
    args = parser.parse_args()
    path = args.path
    
    if path.isdir():
        main(path)
    else:
        print("Invalid directory")
    
