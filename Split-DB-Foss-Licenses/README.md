## Split-SPDX-licenses

Initially Split is being done on Original [SPDXlicenses](Original-SPDX-Dataset) and [Fosslicenses](Original-DB-Foss-Dataset) using "Sliding Window" approach, i.e for a file having 4 paras, there will be these combinations : para1, para2, para3, para4, para1+para2, para2+para3, para3+para4, para1+para2+para3, para2+para3+para4, para1+para2+para3+para4.  

<img src="static\images\slidingwindow.PNG" alt="sliding-window" width="700"/>

The CLI command to do initial split is:

*Make sure to add directory path that need to be splitted.*

```
 python ./Script-Initial-Split/initial_split.py
```
