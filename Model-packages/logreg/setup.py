#!/usr/bin/env python3


"""
 Copyright (C) 2022 Sushant Kumar (sushantmishra02102002@gmail.com)
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

from os import path
from io import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# fetch the long description from the README.md
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="logreg",
    version="0.1.0",
    author="Sushant Kumar",
    author_email="sushantmishra02102002@gmail.com",
    description=(
        "A logisticregression model for predicting license short_name"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        'logreg': [
            'data/logreg',
        ]
    },
    python_requires=">=3.5"
)
