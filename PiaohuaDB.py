#from __future__ import unicode_literals
#-*- coding:utf-8 -*-
import MySQLdb
import sys
from FuncBox import *

class PiaohuaDB(object):
    dbconn = None
    dbcur = None
    sqlQueue = []

    def __init__(self, db_name, host_ip):
        # type: () -> object
        self.dbconn = MySQLdb.connect(
            host=host_ip, user='root', passwd='root', port=3306, charset = 'utf8')
        self.dbcur = self.dbconn.cursor()
        self.dbconn.select_db(db_name)

    def __del__(self):
        self.dbcur.close()
        self.dbconn.close()

    def piaohua_type2tmp_table(self, type_param):
        execute_sql = 'INSERT INTO tmp(id,name,type,url)SELECT id,name,type,url FROM piaohua WHERE type = "%s";' % (
            type_param)
        print execute_sql
        self.dbcur.execute(execute_sql)
        self.dbconn.commit()

    def execute_sql(self):
        while self.sqlQueue:
            sqlstr = self.sqlQueue.pop()
            print sqlstr
            self.dbcur.execute(sqlstr[0], sqlstr[1])
        self.dbconn.commit()

    def IsRecExist(self, cursql):
        pass

    def UpdatePiaohuaTable(self, id, url):
        self.dbcur.execute(
            "UPDATE piaohua SET url = '%s' WHERE ID = '%s';" % (url, id))
        self.dbconn.commit()

    @methodName
    def insert_resource_center_table(self, par, param):
        fields = ['id', 'type', 'name', 'url', 'link', 'about', 'duration', 'country', 'classify', 'imdb']

        sqlstr = 'INSERT INTO resource_center('
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['"%s"' for i in fields])
        sqlstr += ')'

        film_type = par[1].replace('"', '&quot;')
        film_name = par[2].replace('"', '&quot;')
        film_url = par[3].replace('"', '&quot;')
        link = param['link'].replace('"', '&quot;')
        about = param['about'].replace('"', '&quot;')
        about = about.replace('&nbsp;', '')
        about = about.replace('　', '')

        duration = re.findall('◎年代(.*?)◎', about, re.S)
        country = re.findall('◎国家(.*?)◎', about, re.S)
        classify = re.findall('◎类别(.*?)◎', about, re.S)
        imdb = re.findall('◎IMDB评分(.*?)◎', about, re.S)

        duration = duration[0] if duration else ''
        country = country[0] if country else ''
        classify = classify[0] if classify else ''
        imdb = imdb[0] if imdb else ''

        execute_sql = sqlstr % (
            param['id'], film_type, film_name, film_url, link, about, duration, country, classify, imdb)
        print "\033[1;32;40m %s \033[0m" % (film_name)
        print execute_sql.encode('utf-8')
        self.dbcur.execute(execute_sql.encode('utf-8'))
        self.dbconn.commit()

    # tmp or unresolved_issues table operation
    @methodName
    def del_row_from_id_table(self, table_name, id):
        self.dbcur.execute("DELETE FROM %s WHERE id='%s';" % (table_name, id))
        self.dbconn.commit()

    @methodName
    def single_insert_tmp_table(self, table_name, param=[]):
        fields = ['id', 'type', 'name', 'url']

        sqlstr = 'INSERT INTO %s(' % (table_name)
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['"%s"' for i in fields])
        sqlstr += ')'

        param[1] = param[1].replace('"', '&quot;')
        param[2] = param[2].replace('"', '&quot;')
        param[3] = param[3].replace('"', '&quot;')
        execute_sql = sqlstr % (param[0], param[1], param[2], param[3])
        print execute_sql.encode('utf-8')
        self.dbcur.execute(execute_sql.encode('utf-8'))
        self.dbconn.commit()

    @methodName
    def muilt_insert_tmp_table(self, table_name, param=[]):
        fields = ['id', 'type', 'name', 'url']

        sqlstr = 'INSERT INTO %s(' % (table_name)
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['"%s"' for i in fields])
        sqlstr += ')'

        param[1] = param[1].replace('"', '&quot;')
        param[2] = param[2].replace('"', '&quot;')
        param[3] = param[3].replace('"', '&quot;')
        sql_queue = [sqlstr % (item[0], item[1], item[2], item[3]) for item in param]
        while sql_queue:
            self.dbcur.execute(sql_queue.pop())
            self.dbconn.commit()

    def query_tmp_table(self):
        self.dbcur.execute("SELECT id,type,name,url FROM tmp;")
        rows = self.dbcur.fetchall()  # all rows in table
        return rows

    def query_update_log(self):
        self.dbcur.execute("SELECT update_date, url FROM update_log;")
        logs = self.dbcur.fetchall()  # all rows in table
        return logs

    def update_log(self):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        execute_sql = '''UPDATE update_log SET update_date="%s" WHERE film="piaohua";''' % (date_str)
        self.dbcur.execute(execute_sql.encode('utf-8') )
        self.dbconn.commit()
    #

    def seiriContentsTableSQL(self, sType, name, param):
        self.dbcur.execute(
            '''
            create table if not exists juzimi_contents(
              "id" VARCHAR(32) NOT NULL PRIMARY KEY,
              "origin" VARCHAR(64),
              "type" VARCHAR(32),
              "content" TEXT,
              "content_md5"  VARCHAR(128),
              "state" VARCHAR(32),
              "create_time" TIMESTAMP,
              "update_time" TIMESTAMP
            )
            '''
        )
        self.dbconn.commit()

        fields = ['id', 'origin', 'type', 'content',
                  'content_md5', 'state', 'create_time', 'update_time']

        sqlstr = 'INSERT INTO juzimi_contents('
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['%s' for i in fields])
        sqlstr += ')'

        self.sqlQueue = []
        for item in param:
            if not item['origin']:
                item['state'] = 'Null'
            elif item['origin'] != name:
                item['state'] = 'Problem'
            item['type'] = sType
            self.sqlQueue.append(
                (sqlstr, (item['id'],
                          item['origin'],
                          item['type'],
                          item['content'],
                          item['content_md5'],
                          item['state'],
                          item['create_time'],
                          item['update_time'])
                 )
            )

    def QueryPiaohuaTable(self):
        self.dbcur.execute("SELECT * FROM piaohua;")
        rows = self.dbcur.fetchall()  # all rows in table
        return rows

    def DelPiaohuaTable(self, id):
        self.dbcur.execute("DELETE FROM piaohua WHERE id='%s';" % (id))
        self.dbconn.commit()

    def query_type_table(self, type_param):
        self.dbcur.execute(
            "SELECT * FROM piaohua WHERE type='%s';" % (type_param))
        rows = self.dbcur.fetchall()  # all rows in table
        return rows

    def Uniquerows(self):
        pass

    @methodName
    def seiri_piaohua_table_sql(self, table_name, param):
        fields = ['id', 'type', 'name', 'url']

        sqlstr = 'INSERT INTO %s(' % (table_name)
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['%s' for i in fields])
        sqlstr += ')'

        self.sqlQueue = [
            (sqlstr, (item['id'],
                      item['type'],
                      item['name'],
                      item['url'])) for item in param]
