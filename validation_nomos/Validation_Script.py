import json
import pandas as pd
  
f = open("C:/Users/Documents/GSOC21/validatedngram.json",)
data = json.load(f)
df = pd.DataFrame()

for i in data['results']:
	if i["licenses"] != ['No_license_found'] and  i["licenses"] != ['UnclassifiedLicense']:
		dict_new = i
		df = df.append(dict_new, ignore_index=True)

df2 = pd.DataFrame(df.licenses.values.tolist(),columns=['labe_l','label_2','label_3'])
final = pd.concat([df, df2], axis=1, ignore_index=False)
final.drop(["licenses"], axis=1, inplace=True)
final.to_csv("ngram_validated_results.csv",index=False)
f.close()