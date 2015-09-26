# StoneDB 
Simple single-file database engine

This project related to [DMD](https://github.com/abcdw/inno/tree/master/DMD) course.

Created by:

Andrew Tropin (andrewtropin@gmail.com),

Konstantin Sozykin (gogolgrind@gmail.com, gogolgrind@yandex.ru),

Diana Davletshina(d.davletshina@innopolis.ru).

## Database and Data Modeling Course Project. Phase  1.

### ER-diagram
![ER-diagram](https://raw.githubusercontent.com/abcdw/StoneDB/master/report/pics/er_diag.jpg)

\newpage

### Description
Our model of project data base consist 7 relationships, which are:

* keyword(__kid__, value)
* author(__aid__, name)
* venue(__vid__, name)
* paper(__pid__, title, year, venue_id)
* writes(__wid__, paper_id, author_id)
* refs(__rid__, from_id, to_id)
* contains(__cid__, paper_id, keyword_id)

Bold font is used to determine primary keys. 

To determine authors of articles we have Writes entity, which contains paper id and author id as foreign keys.
An article can have references and keywords. We keep keywords in the entity Keyword. To know which keywords article contains we have an entity Contains with attributes - foreign keys: paper id and keyword id. References are organized in an entity Refs. In Refs the atribute 'from id' is a foreign key to article id which has the reference,  the atrribute 'to id' is  a foreign key to article id which is a reference itself.



### Funcionality

1. Select, Insert, delete, and update publication records:
```
SELECT * FROM paper 
INSERT INTO paper VALUES ...
DELETE FROM paper WHERE pid = ...
UPDATE paper SET title = '...' 
```
2. Search for publications based on author name:
```
SELECT * 
FROM paper AS p, author AS a 
WHERE p.pid = a.aid AND a.name = '...'
```
3. Search for publications based on publication year:
```
SELECT * 
FROM paper 
WHERE year = ...
```
4. Search for publications based on venue:
```
SELECT * 
FROM paper AS p, venue as v 
WHERE p.venue_id = v.vid AND v.name LIKE '%..%'
```
5. Search for publications based on title:
```
SELECT * 
FROM paper 
WHERE title LIKE '%...%'
```
6. Search for publications based on keyword:
```
SELECT p.* 
FROM paper AS p, keyword AS k, contains AS c 
WHERE p.pid = c.paper_id AND k.kid = c.keyword_id AND k.value = LIKE '%...%'
```
7. Search for related articles. Method 1:
```
SELECT * 
FROM paper AS p 
WHERE pid IN ( SELECT to_id FROM refs WHERE from_id = ...)
```
Search for related articles. Method 2:
```
SELECT p.* 
FROM paper as p, refs as r 
WHERE r.to_id = p.pid
```
8. Paper sorting based on its popularity that we define from counting the number of articles that have reference to it:
```
SELECT p.pid, COUNT(r.to_id) 
FROM paper AS p, refs AS r 
WHERE p.pid = r.to_id GROUP BY p.pid ORDER BY COUNT(r.to_id) DESC
```
Paper sorting based on count of references:
```
SELECT p.pid, COUNT(r.from_id) 
FROM paper AS p, refs AS r 
WHERE p.pid = r.from_id GROUP BY p.pid 
ORDER BY COUNT(r.from_id) DESC
```
Paper sorting based on relevance:
```
SELECT * from paper ORDER BY year
```

Data for this database was taked from aminer.org[1]. This data set can be used for many research purpose. Also little python3 script[2] was implemented for parsing this data set to psql database.


### References
1. https://aminer.org/billboard/citation
2. https://github.com/abcdw/StoneDB/blob/master/src/utils/upload_data.py
3. https://github.com/abcdw/StoneDB/blob/master/src/psql_py_sripts.py
