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
import argparse


def main(path):
    file = []
    count = []

    for filename in os.listdir(path):
        file.append(filename)
        # dir is your directory path
        lst = os.listdir(os.path.join(path, filename))
        number_files = len(lst)
        count.append(number_files)

    data = pd.DataFrame({"files": file, "count": count})
    data.to_csv("Count.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', help='Pass a directory to find original licenses')

    args = parser.parse_args()

    try:
        path = args.path
        if not os.path.isdir(path):
            raise TypeError
    except TypeError:
        print("Valid directory not provided")

    main(path)
