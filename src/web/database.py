# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:26:39 2015
on python3
@author: Konstantin Sozykin
tested on windows
"""

import psycopg2

def do_query(query,dbname,user,passw,server = 'localhost'):
    try:
        conn = psycopg2.connect("dbname=" + dbname + " user=" + user +" host= " + server  + " password=" + passw)
    except:
        print("Can't conntect to " + dbname)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except:
        print("Can't execute")
    result_rows = cur.fetchall()
    conn.close()
    return result_rows

def search_by_year(year,dbname,user,passw,server = 'localhost'):
    q = "SELECT * FROM paper WHERE year =" + year
    return do_query(q,dbname,user,passw)

def search_by_title(pattern,dbname,user,passw,server = 'localhost'):
    q = "SELECT * FROM paper WHERE title LIKE '%"+ pattern +"%'"
    return do_query(q,dbname,user,passw)

def search_by_author(pattern,dbname,user,passw,server = 'localhost'):
    q = "SELECT * FROM paper AS p, author AS a WHERE p.pid = a.aid AND a.name = '" + pattern + "'"
    return do_query(q,dbname,user,passw)

def search_by_venue(pattern,dbname,user,passw,server = 'localhost'):
    q = "SELECT * FROM paper AS p, venue as v WHERE p.venue_id = v.vid AND v.name LIKE '%"+ pattern +"%'"
    return do_query(q,dbname,user,passw)

def search_by_keyword(pattern,dbname,user,passw,server = 'localhost'):
    q = "SELECT p.* FROM paper AS p, keyword AS k, contains AS c WHERE p.pid = c.paper_id AND k.kid = c.keyword_id AND k.value = LIKE '%"+ pattern +"%'"
    return do_query(q,dbname,user,passw)

def search_related_article(pattern,dbname,user,passw,server = 'localhost'):
    q = "SELECT * FROM paper AS p WHERE pid IN ( SELECT to_id FROM refs WHERE from_id = " + pattern + ")"
    return do_query(q,dbname,user,passw)

def search_related_article2(dbname,user,passw,server = 'localhost'):
    q = "SELECT p.* FROM paper as p, refs as r WHERE r.to_id = p.pid"
    return do_query(q,dbname,user,passw)

def sort_by_popularity(dbname,user,passw,server = 'localhost'):
    q = "SELECT p.pid, COUNT(r.to_id) FROM paper AS p, refs AS r WHERE p.pid = r.to_id GROUP BY p.pid ORDER BY COUNT(r.to_id) DESC"
    return do_query(q, dbname,user,passw)

def sort_by_count_refs(dbname,user,passw,server = 'localhost'):
    q = "SELECT p.pid, COUNT(r.from_id) FROM paper AS p, refs AS r WHERE p.pid = r.from_id GROUP BY p.pid ORDER BY COUNT(r.from_id) DESC"
    return do_query(q, dbname,user,passw)

def sort_by_year(dbname,user,passw,server = 'localhost'):
    q = "SELECT * from paper ORDER BY year"
    return do_query(q, dbname,user,passw)

def insert_values(table_name,values,dbname,user,passw,server = 'localhost'):
    query = "INSERT INTO " + table_name + " VALUES " + values
    try:
        conn = psycopg2.connect("dbname=" + dbname + " user=" + user +" host= " + server  + " password=" + passw)
    except:
        print("Can't conntect to " + dbname)
    cur = conn.cursor()
    try:
        cur.execute(query)
    except:
        print("Can't execute")
    conn.commit()
    conn.close()

def delete_paper_by_id(pid, dbname,user,passw,server = 'localhost'):
    query = "DELETE FROM paper WHERE pid = " + pid
    try:
        conn = psycopg2.connect("dbname=" + dbname + " user=" + user +" host= " + server  + " password=" + passw)
    except:
        print("Can't conntect to " + dbname)
    cur = conn.cursor()
    try:
        cur.execute(query)
        ##print("Can execute")
    except:
        print("Can't execute")
    conn.commit()
    conn.close()

