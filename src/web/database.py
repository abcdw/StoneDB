# coding: utf-8
# import psycopg2
import btree

class Paper:
    def __init__(self):
        self.data = {}
        self.data['title'] = ''
        self.data['year'] = ''
        self.data['id'] = ''
        self.data['vid'] = ''
        self.data['author'] = ''
        self.fields = []

    def update(self, line):
        line = line.strip()
        if line.startswith('#*'):
            self.data['title'] = line[2:]
        if line.startswith('#t'):
            self.data['year'] = line[2:]
        if line.startswith('#c'):
            self.data['vid'] = line[2:]
        if line.startswith('#i'):
            self.data['id'] = line[2:]
        if line.startswith('#@'):
            self.data['author'] = line[2:]

    def set_projection(self, *args):
        self.fields = args

    def get_tuple(self):
        result = []
        for arg in self.fields:
            if arg in self.data.keys():
                result.append(self.data[arg])
        return tuple(result)


    @property
    def tuple(self):
        return self.get_tuple()

    @property
    def title(self):
        return self.data['title']

    @property
    def year(self):
        return self.data['year']

    @property
    def id(self):
        return self.data['id']

    @property
    def author(self):
        return self.data['author']


class DBMS:

    def __init__(self, dbname, user, passw, server):
        self.dbname = dbname
        self.user = user
        self.passw = passw
        self.server = server
        self.papers = []
        self.b_plus_tree = btree.BPlusTree(2)
        self.data_file = 'publications_new.txt'
        self.projection_fields = ()

        with open(self.data_file) as f:
            i = 0
            p = Paper()

            for line in f:
                i = i + 1
                if i > 100000:
                    break
                p.update(line)

                if line.strip() == '':
                    self.papers.append(p)
                    p = Paper()

    def set_projection(self, *args):
        self.projection_fields = args
        for paper in self.papers:
            paper.set_projection(*args)


    def group_by_year(self, **kwargs):

        years = set(map(lambda x: x.year, self.papers))
        count = {}
        for year in years:
            count[year] = 0

        if kwargs['func'] == 'count':
            for paper in self.papers:
                count[paper.year] = count[paper.year] + 1

        for year in years:
            yield (year, count[year])

    def join_paper_author(self, *args, **kwargs):
        authors_enum = enumerate(set(map(lambda x: x.author, self.papers)))
        authors = {}
        for author in authors_enum:
            authors[author[1]] = author[0]

        for paper in self.papers:
            row = (paper.id, paper.title, authors[paper.author],
                   authors[paper.author], paper.author)
            yield row

    def do_query(self, query):
        try:
            conn = psycopg2.connect("dbname=" + self.dbname + " user=" + self.user +" host= " + self.server  + " password=" + self.passw)
        except:
            print("Can't conntect to " + self.dbname)
        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print("Can't execute")
        result_rows = cur.fetchall()
        conn.close()
        return result_rows

    def search_by_year(self, year):
        q = "SELECT * FROM paper WHERE year =" + year
        return self.do_query(q)

    def search_by_title(self, pattern):
        result = filter(lambda x: x.title.decode('utf-8').encode('utf-8').find(pattern.encode('utf-8')) != -1, self.papers)
        return result

    def sort_by_title(self, papers):
        return sorted(papers, key=lambda x: x.title)

    def search_by_author(self, pattern):
        q = "SELECT * FROM paper AS p, author AS a WHERE p.pid = a.aid AND a.name = '" + pattern + "'"
        return self.do_query(q)

    def search_by_venue(self, pattern):
        q = "SELECT * FROM paper AS p, venue as v WHERE p.venue_id = v.vid AND v.name LIKE '%"+ pattern +"%'"
        return self.do_query(q)

    def search_by_keyword(self, pattern):
        q = "SELECT p.* FROM paper AS p, keyword AS k, contains AS c WHERE p.pid = c.paper_id AND k.kid = c.keyword_id AND k.value = LIKE '%"+ pattern +"%'"
        return self.do_query(q)

    def search_related_article(self, pattern):
        q = "SELECT * FROM paper AS p WHERE pid IN ( SELECT to_id FROM refs WHERE from_id = " + pattern + ")"
        return self.do_query(q)

    def search_related_article2(self):
        q = "SELECT p.* FROM paper as p, refs as r WHERE r.to_id = p.pid"
        return self.do_query(q)

    def sort_by_popularity(self):
        q = "SELECT p.pid, COUNT(r.to_id) FROM paper AS p, refs AS r WHERE p.pid = r.to_id GROUP BY p.pid ORDER BY COUNT(r.to_id) DESC"
        return self.do_query(q)

    def sort_by_count_refs(self):
        q = "SELECT p.pid, COUNT(r.from_id) FROM paper AS p, refs AS r WHERE p.pid = r.from_id GROUP BY p.pid ORDER BY COUNT(r.from_id) DESC"
        return self.do_query(q)

    def sort_by_year(self):
        q = "SELECT * from paper ORDER BY year"
        return self.do_query(q)

    def select_by_id(self, id):
        q = "SELECT * from paper WHERE pid=" + id
        return self.do_query(q)

    def get_max_id(self):
        q = "SELECT MAX(pid) FROM paper"
        return self.do_query(q)[0][0]

    def insert_to_paper(self, title, year, vid):
        pid = int(self.papers[-1].id) + 1
        #query = "INSERT INTO paper VALUES ('" + pid + "', '" + title + "', '" + year + "', '" + vid + "')"
        p = Paper()
        p.id = pid
        p.title = title
        p.year = year
        p.vid = vid
        self.papers.append(p)
        return p

    def update_paper(self, pid, title, year, vid):
        #query = "UPDATE paper SET title = '" + title + "', year = '" + year + "', venue_id = '" + vid + "' WHERE pid = " + pid
        p = filter(lambda x: x.id == str(pid), self.papers)[0]
        p.title = title
        p.year = year
        p.vid = vid

    def insert_values(self, table_name, values):
        query = "INSERT INTO " + table_name + " VALUES " + values
        return self.do_query(query)

    def delete_paper_by_id(self, pid):
        #query = "DELETE FROM paper WHERE pid = " + pid
        papers = filter(lambda x: x.id == str(pid), self.papers)
        if papers:
            p = papers[0]
            self.papers.remove(p)

    def write_index(self):
        last = 100000
        for paper in self.papers[:last]:
            tuple_ = [paper.id,paper.title,paper.year,paper.vid]
            self.b_plus_tree.insert(paper.title,tuple_)
        with open(self.data_file,"a+") as f:
            for item in self.b_plus_tree.items():
                key = str(item[0])
                value = '-'.join(map(str,item[1]))
                #print key,value,'\n'
                f.write(key + ' ' + value + '\n')


if __name__ == '__main__':
    db = DBMS("wqer", "qwer", "wqer", "qwer")
    # db.set_projection('id', 'title', 'id')
    # papers = db.sort_by_title(db.search_by_title("a"))
    # for paper in papers:
    #     print paper.tuple


    # result = db.group_by_year(func='count') # example of cursor
    # for obj in result:
    #     print obj

    for obj in db.join_paper_author(on='p.aid == a.id'):
        print obj

    # TODO: check frontend
    # TODO: join
    # TODO: group_by

    # TODO: db.join_something()


