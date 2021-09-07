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
import random
from collections import defaultdict


def regex_expansion(prevsen, latersen, text):
    result = []
    while(len(result) < 100):
        final_regex = ""
        num = random.randint(1, 4)
        for i in range(num):
            final_regex = final_regex + \
                generate_sen(markov_chain(text),
                             random.randint(1, 32), text)+" "
        fregex_ = prevsen + final_regex + latersen
        ans = licensestatement_(fregex_)
        for i in ans:
            i = re.sub("[\s]+", " ", i)
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
        except Exception:
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
