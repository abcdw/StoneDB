
import psycopg2
class DBMS:

    def __init__(self, dbname, user, passw, server):
        self.dbname = dbname
        self.user = user
        self.passw = passw
        self.server = server

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
        q = "SELECT * FROM paper WHERE title LIKE '%"+ pattern +"%'"
        return self.do_query(q)

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

    def get_max_id(self):
        q = "SELECT MAX(pid) FROM paper"
        return self.do_query(q)[0][0]

    def insert_to_paper(self, title, year, vid):
        pid = str(self.get_max_id() + 1)
        query = "INSERT INTO paper VALUES ('" + pid + "', '" + title + "', '" + year + "', '" + vid + "')"
        print query
        try:
            conn = psycopg2.connect("dbname=" + self.dbname + " user=" + self.user + " host= " + self.server  + " password=" + self.passw)
        except:
            print("Can't connect to " + self.dbname)
        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print("Can't execute")
        conn.commit()
        conn.close()

    def update_paper(self, pid, title, year, vid): # pid is current value
        query = "UPDATE paper SET title = '" + title + "', year = '" + year + "', venue_id = '" + vid + "' WHERE pid = " + pid
        print query
        try:
            conn = psycopg2.connect("dbname=" + self.dbname + " user=" + self.user + " host= " + self.server  + " password=" + self.passw)
        except:
            print("Can't connect to " + self.dbname)
        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print("Can't execute")
        conn.commit()
        conn.close()

    def insert_values(self, table_name,values):
        query = "INSERT INTO " + table_name + " VALUES " + values
        try:
            conn = psycopg2.connect("dbname=" + self.dbname + " user=" + self.user +" host= " + self.server  + " password=" + self.passw)
        except:
            print("Can't conntect to " + self.dbname)
        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print("Can't execute")
        conn.commit()
        conn.close()

    def delete_paper_by_id(self, pid):
        query = "DELETE FROM paper WHERE pid = " + pid
        try:
            conn = psycopg2.connect("dbname=" + self.dbname + " user=" + self.user +" host= " + self.server  + " password=" + self.passw)
        except:
            print("Can't conntect to " + self.dbname)
        cur = conn.cursor()
        try:
            cur.execute(query)
        except:
            print("Can't execute")
        conn.commit()
        conn.close()

