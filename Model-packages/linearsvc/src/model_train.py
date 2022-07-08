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

import pandas as pd
import pickle
import os
from glob import glob
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


def data():
    folders = glob("Minerva-Dataset-Generation/Split-DB-Foss-Licenses/*")
    license_lists = []
    for folder in folders:
        if os.path.isdir(folder):
            list = [os.path.join(folder, fname)
                    for fname in os.listdir(folder)]
            license_lists.append(list)

    base_lists = []
    license_texts = []
    for license_list in license_lists:
        for license in license_list:
            path = os.path.dirname(license)
            base = os.path.basename(path)
            base_lists.append(base)
            file = open(license)
            file_content = file.read()
            license_texts.append(file_content)

    df = pd.DataFrame({"short_name": base_lists, "text": license_texts})

    df = df.sample(frac=1).reset_index(drop=True)
    df.dropna(inplace=True)
    return df


def train():
    train_data = data()

    X_train = train_data.text
    Y_train = train_data.short_name

    logreg = Pipeline(
        [
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            ("clf", LinearSVC(n_jobs=1, C=1e5)),
        ]
    )
    print("Model training has started!")
    logreg_model = logreg.fit(X_train, Y_train)
    print("Training finished!")

    with open("./linearsvc/data/linearsvc", "wb") as f:
        pickle.dump(logreg_model, f)
    print("Model saved successfully!")


if __name__ == "__main__":
    train()
