import pandas as pd
import os
import shutil
import numpy as np

df = pd.read_csv("C:/Users/Documents/GSOC21/validation_/markov_results.csv")


for i, row in df.iterrows():
   print(row['file'])
   columns = ['labe_l','label_2','label_3']
   for label in columns:
     try:
        if row[label]==np.nan:
          break
        foldername = row[label]
        newfolder = os.path.join("C:/Users/Documents/GSOC21/SPDX-Dataset-updated",foldername)
        if not os.path.exists(newfolder):
          os.makedirs(newfolder)
        dirListing = os.listdir(newfolder)
        file_count = len(dirListing)+1
        name = row['file'].rpartition(".")[0].rpartition("-")[0] +"_"+ str(file_count)+".txt"
        shutil.copy2(os.path.join("C:/Users/Documents/GSOC21/markov-dataset",row['file']),os.path.join(newfolder,name))
     except:
       break

