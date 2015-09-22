# -*- coding: utf-8 -*-
import psycopg2
import sys
import re


class Paper:
    pid = None
    title = None
    author = None
    aid = None
    wid = None
    year = None
    venue = None
    vid = None
    index = None
    references = []
    abstract = None
    keywords = []

    def make_keywords(self):
        if self.abstract:
            tmp_abstract = self.abstract.replace(',', '').replace('.', '')
            not_empty_words = filter(None, tmp_abstract.split(' '))
            self.keywords = map(lambda x: x.lower(), not_empty_words)

    def update(self, line):
        line = line.strip()
        if line.startswith('#*'):
            self.title = line[2:]
        if line.startswith('#@'):
            self.author = line[2:]
        if line.startswith('#t'):
            self.year = line[2:]
        if line.startswith('#c'):
            self.venue = line[2:]
        if line.startswith('#i'):
            self.index = line[2:]
        if line.startswith('#%'):
            if line[2:] != '':
                self.references.append(line[2:])
        if line.startswith('#!'):
            abstract = line[2:]
            if abstract == '':
                abstract = self.title
            self.abstract = abstract
        self.make_keywords()

    def printme(self):
        print self.index
        #  print self.title
        #  print self.author
        #  print self.year
        #  print self.venue
        #  print self.index
        #  print self.references
        #  print self.abstract
        #  print self.keywords
        print ''


class DB:
    def __init__(self):
        self.connection = psycopg2.connect(database="stonedb", user="postgres")
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_or_create_author(self, a):
        cursor = self.cursor
        cursor.execute("SELECT * FROM author WHERE name = %s;", (a,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(aid) FROM author;")
            id = cursor.fetchone()[0] or 0
            cursor.execute("INSERT INTO author (aid, name) VALUES (%s, %s)", (id+1, a,))
            result = (id+1,)
        id = result[0]
        return id

    def get_or_create_venue(self, v):
        cursor = self.cursor
        cursor.execute("SELECT * FROM venue WHERE name = %s;", (v,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(vid) FROM venue;")
            id = cursor.fetchone()[0] or 0
            cursor.execute("INSERT INTO venue (vid, name) VALUES (%s, %s)", (id+1, v,))
            result = (id+1,)
        id = result[0]
        return id

    def get_or_create_paper(self, p):
        cursor = self.cursor
        cursor.execute("SELECT * FROM paper WHERE pid = %s;", (p.index,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(pid) FROM paper;")
            id = cursor.fetchone()[0] or 0
            cursor.execute(
                "INSERT INTO paper (pid, title, year, venue_id) VALUES (%s, %s, %s, %s)",
                (p.index, p.title, p.year, p.vid)
            )
            result = (p.index,)
        id = result[0]
        return id

    def get_or_create_writes(self, p):
        cursor = self.cursor
        cursor.execute("SELECT * FROM writes WHERE wid = %s;", (p.wid,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(wid) FROM writes;")
            id = cursor.fetchone()[0] or 0
            cursor.execute(
                "INSERT INTO writes (wid, paper_id, author_id) VALUES (%s, %s, %s)",
                (id+1, p.pid, p.aid)
            )
            result = (id+1,)
        id = result[0]
        return id

    def get_or_create_keyword(self, kw):
        cursor = self.cursor
        cursor.execute("SELECT * FROM keyword WHERE value = %s;", (kw,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(kid) FROM keyword;")
            id = cursor.fetchone()[0] or 0
            cursor.execute(
                "INSERT INTO keyword (kid, value) VALUES (%s, %s)",
                (id+1, kw)
            )
            result = (id+1,)
        id = result[0]
        return id

    def get_or_create_contains(self, p, kwid):
        cursor = self.cursor
        cursor.execute("SELECT * FROM contains WHERE cid = %s;", (0,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(cid) FROM contains;")
            id = cursor.fetchone()[0] or 0
            cursor.execute(
                "INSERT INTO contains (cid, paper_id, keyword_id) VALUES (%s, %s, %s)",
                (id+1, p.pid, kwid)
            )
            result = (id+1,)
        id = result[0]
        return id

    def get_or_create_references(self, p, to_id):
        cursor = self.cursor
        cursor.execute("SELECT * FROM refs WHERE rid = %s;", (0,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("SELECT MAX(rid) FROM refs;")
            id = cursor.fetchone()[0] or 0
            cursor.execute(
                "INSERT INTO refs (rid, from_id, to_id) VALUES (%s, %s, %s)",
                (id+1, p.pid, to_id)
            )
            result = (id+1,)
        id = result[0]
        return id

    def insert_paper(self, p):
        cursor = self.cursor
        try:
            p.vid = self.get_or_create_venue(p.venue)
            p.pid = self.get_or_create_paper(p)
            p.aid = self.get_or_create_author(p.author)
            p.wid = self.get_or_create_writes(p)
            for kw in p.keywords:
                kwid = self.get_or_create_keyword(kw)
                self.get_or_create_contains(p, kwid)

            for ref_id in p.references:
                self.get_or_create_references(p, ref_id)

        except Exception, e:
            raise e

        pass


def read_dataset():
    # do sed 's/#index/#i/' publications.txt > publications_new.txt before use
    # script
    data_file = '/home/abcdw/tmp/dblp/DBLP_Citation_2014_May/publications_new.txt'

    with DB() as db:
        with open(data_file) as f:
            i = 0
            p = Paper()

            for line in f:
                i = i + 1
                if i > 3000:
                    break
                p.update(line)

                if line.strip() == '':
                    #  if p.abstract:
                    #  p.printme()
                    db.insert_paper(p)
                    p = Paper()


read_dataset()
