<h1 align="center">Minerva Dataset Generation<img src="assets\wcoding.giff" width="80"></h1>
<h2 align="center">Project Overview</h2>

<p align="center">
        <img src="assets\project_overview.png" width="800" height="400">
</p>

![ViewCount](https://views.whatilearened.today/views/github/fossology/Minerva-Dataset-Generation.svg)
![GitHub](https://img.shields.io/github/followers/fossology?style=social)
![GitHub Stars](https://img.shields.io/github/stars/fossology/Minerva-Dataset-Generation?style=social)

Why there is a need to generate a dataset?
1. To implement any Machine learning/Deep learning algorithm we need a better and bigger dataset of SPDX Licences. Due to the lack of dataset currently, all the 10 algorithms which have been tested on Atarashi are restricted to 59% accuracy. But unfortunately, there exists no such dataset for open source licenses on the web.
2. Advanced Architectures and algorithms such as LSTMs, GRU, BERT, WordNET, etc. require huge volumes of the dataset before achieving the ability to outperform the accuracy of even traditional algorithms such as TF-IDF, n-gram, etc. 
3. Licenses differ from traditional corpora, because of which 50-60% keywords are similar in any two licenses, and if the licenses have the same license heading but different versions, they're around 90% similar.

<p align="center">
        <img src="assets\work.gif" width="400" height="300">
</p>

#### SPDX recent release : [SPDX](https://spdx.org/licenses/licenses.json)
```
 python ./Download-licenses-Script/spdx.py
```
#### SPDX-exceptions recent release : [SPDX-exceptions](https://spdx.org/licenses/exceptions.json)
```
 python ./Download-licenses-Script/exceptions.py
```
#### Licenses in Fossology Database : [licenseRef](https://raw.githubusercontent.com/fossology/fossology/master/install/db/licenseRef.json)
```
 python ./Download-licenses-Script/database-foss.py
```

### GENERATED FILES THROUGH INITIAL SPLIT
The basic idea is n-gramming licenses and maintaining a sliding window, i.e for a licene with 4 paragraphs, all the different files that I wanted to generate were - <i>para1, para2, para3, para4, para1+para2, para2+para3, para3+para4, para1+para2+para3, para2+para3+para4, para1+para2+para3+para4.</i>
<i>Not para1+para3, para1+para3+para4, etc. because the structure of licenses needs to be maintained.</i>
```
 python ./Script-Initial-Split/initial_split.py
```
Script : [initial_split](https://github.com/fossology/Minerva-Dataset-Generation/tree/main/Script-Initial-Split)
</br>
Files : [SPDX](https://github.com/fossology/Minerva-Dataset-Generation/tree/main/Split-SPDX-licenses)
</br>
Files : [FOSSologyDatabase](https://github.com/fossology/Minerva-Dataset-Generation/tree/main/Split-DB-Foss-Licenses)

### ADDING REGEX TO FILES
Regex from [STRINGS.in](https://github.com/fossology/Minerva-Dataset-Generation/tree/main/STRINGSin-Regex-Extraction) file is added to splitted files. Regex expansion is done through free and open-source libraries such as [xeger](https://pypi.org/project/xeger/), [intxeger](https://pypi.org/project/intxeger/) 

<p align="center">
        <img src="assets\regexsplit.png" width="400">
</p>

### HANDLING REGEX EXPANSION
To handle expansions i.e .{1,32}, .{1,64} two algorithms are being considered : 

A. NGRAM
</br>
<i>(basically a set of co-occurring words within a given window)</i>
</br>
B. MARKOV
</br>
<i>(As an extension of Naive Bayes for sequential data, the Hidden Markov Model provides a joint distribution over the letters/tags with an assumption of the dependencies of variables x and y between adjacent tags.)</i>

Added "Multiprocessing" to the Script to speed up the process of data generation.

Codebase : [Ngram](https://github.com/fossology/Minerva-Dataset-Generation/tree/main/ngram)
</br>
To generate licenses with ngram expansion:
```
 python ./ngram/licenses.py
```
Codebase : [Markov](https://github.com/fossology/Minerva-Dataset-Generation/tree/main/markov)
</br>
To generate licenses with ngram expansion:
```
 python ./markov/markov_licenses.py
```

### Validating Dataset Generated Using NOMOS in Fossology
Using Nomos to validate generated files. This is a base line <i>regex-based</i> validation for the generated text files using both the algorithms. Terminal command to run this will be  : 
```
 sudo nomos -J -d <folder_with_files>
```
And to use multiple cores to validate files (here I am using 3 cores) :
```
 sudo nomos -J -d <folder_with_files> -n 3
```