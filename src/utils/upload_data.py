# -*- coding: utf-8 -*-
import psycopg2
import sys
import re


class Paper:
    title = None
    author = None
    year = None
    venue = None
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
        print self.title
        print self.author
        print self.year
        print self.venue
        print self.index
        print self.references
        print self.abstract
        print self.keywords
        print ''


# Init dabase connection
connection = psycopg2.connect(database="movies", user="postgres")
cursor = connection.cursor()

def insert_paper(cursor, p):
    pass


def read_dataset():
    # do sed 's/#index/#i/' publications.txt > publications_new.txt before use
    # script
    data_file = '/home/abcdw/tmp/dblp/DBLP_Citation_2014_May/publications_new.txt'

    with open(data_file) as f:
        i = 0
        p = Paper()

        for line in f:
            i = i + 1
            if i > 20000000:
                break
            p.update(line)

            if line.strip() == '':
                if p.abstract:
                    p.printme()
                p = Paper()


read_dataset()
