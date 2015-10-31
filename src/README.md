# StoneDB 
Simple single-file database engine

This project related to [DMD](https://github.com/abcdw/inno/tree/master/DMD) course.

Created by:

Andrew Tropin (andrewtropin@gmail.com),

Konstantin Sozykin (gogolgrind@gmail.com, gogolgrind@yandex.ru),

Diana Davletshina(d.davletshina@innopolis.ru).

## Database and Data Modeling Course Project. Phase  2.

## Abstract 

During phase 2 web-application was created. Our web-interface allows users to following functionality:

* Retrive articles, filter article list.
* Create new article. (requires authentication)
* Modify existing article. (requires authentication)
* Delete existing article. (requires authentication)

## Deployment process

Retrive source code from git repository to your local machine with following command:
```
git clone https://github.com/abcdw/StoneDB
```

Install necessary dependencies for backend app:
```
cd StoneDB/src
pip install -r web/requirements.txt
```

Initializate database with following commands:
```
pg_restore -U postgres -p < sql/schema.sql
pg_restore -U postgres -p < sql/data.sql
```

Run web-server with following command:
```
python web/__init__.py
```

Enjoy. Login/password: admin/admin 

## Description of source code.

* web/__init__.py - flask application, that handles browser requests from user and response. Uses web/database.py for database operations. Authenticate and authorize user.
* web/database.py - makes database operations and returns python objects.
* web/templates/table.html - main page with article list and links to another pages
* web/templates/create_article.html - page that allows you to create article.
* web/templates/update_article.html - page that allows you to update and delete existing article.
* web/templates/redirect.html - page that redirects to page some url.
* utils/upload_data.py - parser that fills database with articles and other entries.
* utils/wipe_db.sh - scripts that wipes database and init it with sql/schema.sql
* sql/schema.sql - file that contains database schema.

##Screenshot of User Web Interface.
### Creating  new record in DB
![Creating of new record in DB](https://raw.githubusercontent.com/abcdw/StoneDB/master/pics/create_article.png)
### Updating new record in DB
![Updating of new record in DB](https://raw.githubusercontent.com/abcdw/StoneDB/master/pics/update_article.png)
### Table View
![View of table](https://raw.githubusercontent.com/abcdw/StoneDB/master/pics/table.png)

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
An article can have references and keywords. We keep keywords in the entity Keyword. To know which keywords article contains we have an entity Contains with attributes - foreign keys: paper id and keyword id. References are organized in an entity Refs which is actually a weak entity. In Refs the atribute 'from id' is a foreign key to article id which has the reference,  the atrribute 'to id' is  a foreign key to article id which is a reference itself.



### Funcionality

1. Select, Insert, delete, and update publication records:
```
SELECT * FROM paper 
INSERT INTO paper VALUES ...
DELETE FROM paper WHERE pid = ...
UPDATE paper SET title = '...' 
```

It is more efficient and convenient to insert data about publication using python script as we did. While adding data to paper table we can automatically create necessary tuples in keyword and references tables.

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
Paper sorting based on actuality:
```
SELECT * from paper ORDER BY year
```
Paper sorting based on count of references:
```
SELECT p.pid, COUNT(r.from_id) 
FROM paper AS p, refs AS r 
WHERE p.pid = r.from_id GROUP BY p.pid 
ORDER BY COUNT(r.from_id) DESC
```


Data for this database was taked from aminer.org[1]. This data set can be used for many research purpose. Also little python3 script[2] was implemented for parsing this data set to psql database.


### References
1. https://aminer.org/billboard/citation
2. https://github.com/abcdw/StoneDB/blob/master/src/utils/upload_data.py
3. https://github.com/abcdw/StoneDB/blob/master/src/psql_py_sripts.py
4. Main repository link : https://github.com/abcdw/StoneDB
