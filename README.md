# <img align="left" width=100px alt="Unicorn" src="https://media.giphy.com/media/3ohs4BSacFKI7A717y/giphy.gif" /> MINERVA-Dataset-Generation 




<img src="https://user-images.githubusercontent.com/50830709/125133165-0e014000-e123-11eb-9890-3510887deaac.JPG" alt="project-overview" width="700"/>


### Validating Dataset Generated Using NOMOS in Fossology
Nomos helps to label the licenses, with license_header, or Unclassidied_licenses, No_License_found, Public-domain, Restricted, etc. This acts like a base line validation of the generated text files using both the algorithms. Terminal command to run this will be  : 
```
 sudo nomos -J -d <folder_with_files>
```
And to use multiple cores to validated the files (here I am using 3 cores) :
```
 sudo nomos -J -d <folder_with_files> -n 3
```



