import re
from pathlib import Path
import pandas as pd

def extract(content):
  content = re.split('\n\n',content)
  result = []
  for text in content:
    if text.lstrip().startswith('%'):
      text = text.split('\n\n')
      for j in text:
        j = j.replace("\n"," ")
        result.append(j)

  for i in range(len(result)):
    regex.append(result[i].split("%STR%",1)[1])
    tokens = re.findall("[\w']+", result[i])
    org.append(tokens[1])
    sen = result[i].split("%STR%",1)[0]
  df = pd.DataFrame({'License':org,'Regex':regex})
  df['License'] = df['License'].apply(lambda x: x.replace("_SPDX_",""))
  df.to_csv('SPDXRegex.csv',index=False)

if __name__ == "__main__":
  content = Path("/STRINGS.in-Regex-Extraction/license_regex.txt").read_text() 
  extract(content)

