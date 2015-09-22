# StoneDB 
Simple single-file database engine


This project related to [DMD](https://github.com/abcdw/inno/tree/master/DMD) course.

Database and Data Modeling Course Project. Phase  1.

Create by Andrew Tropin, Konstantin Sozykin, Diana Davletshina.
### ER-diagram
![ER-diagram](https://raw.githubusercontent.com/abcdw/StoneDB/master/report/pics/er_diag.jpg)



### Relations
* keyword(__kid__,value)
* author(__aid__,aname)
* venue(__vid__,vname)
* paper(__pid__,title, pages, year, venue_id)
* writes(__paper_id, author_id__)
* references(__from_id, to_id__)
* contains(__paper_id, keyword_id__)
