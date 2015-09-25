# StoneDB 
Simple single-file database engine

This project related to [DMD](https://github.com/abcdw/inno/tree/master/DMD) course.

Created by Andrew Tropin, Konstantin Sozykin, Diana Davletshina.

## Database and Data Modeling Course Project. Phase  1.

### ER-diagram
![ER-diagram](https://raw.githubusercontent.com/abcdw/StoneDB/master/report/pics/er_diag.jpg)

### Description
Our model of project data base consist 7 relationships, which are:
* keyword(__kid__, value)
* author(__aid__, name)
* venue(__vid__, name)
* paper(__pid__, title, year, venue_id)
* writes(__wid__, paper_id, author_id)
* refs(__rid__, from_id, to_id)
* contains(__cid__, paper_id, keyword_id)

Data for this database was taked from aminer.org[1]. This data set can be used for many research purpose. Also little python3 script[2] was implemented for parsing this data set to psql database.



### References
1. https://aminer.org/billboard/citation
2. https://github.com/abcdw/StoneDB/blob/master/src/utils/upload_data.py
3. link to pyton sql queries

