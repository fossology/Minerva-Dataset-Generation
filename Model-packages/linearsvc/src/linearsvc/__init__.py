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


from pkg_resources import resource_filename
import pickle


class linearsvc():
    def __init__(self, preprocessed_file):
        self.preprocessed_file = preprocessed_file

    def classify(self):
        data = resource_filename("linearsvc", "data/linearsvc")
        with open(data, 'rb') as f:
            Classifier = pickle.load(f)
        return Classifier

    def predict_shortname(self):
        predictor = self.classify()
        return predictor.predict(self.preprocessed_file)
