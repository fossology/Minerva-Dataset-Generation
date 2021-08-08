import os
import pandas as pd
import argparse

def main(path):
    file = []
    count = []

    for filename in os.listdir(path):
        file.append(filename)
        lst = os.listdir(os.path.join(path,filename)) # dir is your directory path
        number_files = len(lst)
        count.append(number_files)           

    data = pd.DataFrame({"files":file,"count":count})
    data.to_csv("Count_SPDX_primary_split.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Pass a directory to find original licenses')
    args = parser.parse_args()
    path = args.path
    main(path)
