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

import string
import re
import intxeger
from collections import defaultdict
import numpy as np
import random


def licensestatement_(regex_):
    x = intxeger.build(regex_)
    res = x.sample(N=1)
    result = res
    i = 2
    while True:
        try:
            result = res
            result = list(set(result))
            if len(result) > 10:
                return result
            res = x.sample(N=i)
            i += 1
        except Exception:
            break
    return result


def regex_expansion(prevsen, input_list, latersen):
    res_ = []
    while(len(res_) < 200):
        final_regex = ""
        num = random.randint(1, 4)
        for i in range(num):
            final_regex = final_regex + \
                np.random.choice(input_list)+" (and|or) "
        fregex_ = prevsen + " " + final_regex + " " + latersen
        ans = licensestatement_(fregex_)
        for i in ans:
            i = re.sub("[\s]+", " ", i)
            res_.append(i)
    return res_


def generate_statements():
    for i in range(2, 20):
        m = create_ngram_model(i, key)

        for i in range(1, len(text)):
            random.seed(i)
            generated_text = m.generate_text(np.random.randint(6, 31))
            generated_text = clean_license(generated_text)
            generated_text = generated_text.lower()
            expansion.append(generated_text)
            expansion = list(set(expansion))
