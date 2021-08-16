# <img align="left" width=100px alt="Unicorn" src="https://media.giphy.com/media/3ohs4BSacFKI7A717y/giphy.gif" /> MINERVA-Dataset-Generation 




<img src="static\images\project_overview.png" alt="project-overview" width="700"/>


### Validating Dataset Generated Using NOMOS in Fossology
We are using Nomos to label the licenses, with license_headers with which it's regex is being matched, or the other labels that are Unclassidied_licenses, No_License_found, Public-domain, Restricted, etc. This is a base line validation for the generated text files using both the algorithms. Terminal command to run this will be  : 
```
 sudo nomos -J -d <folder_with_files>
```
And to use multiple cores to validate files (here I am using 3 cores) :
```
 sudo nomos -J -d <folder_with_files> -n 3
```



