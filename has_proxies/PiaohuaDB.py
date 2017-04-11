from __future__ import unicode_literals
#-*- coding:utf-8 -*-
import psycopg2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(1000000)


class PiaohuaDB(object):
    dbconn = None
    dbcur = None
    sqlQueue = []

    def __init__(self):
        # type: () -> object
        self.dbconn = psycopg2.connect(
            database="piaohua", user="frank", password="root", host="127.0.0.1", port="5432")
        self.dbcur = self.dbconn.cursor()

    def __del__(self):
        self.dbcur.close()
        self.dbconn.close()

    # def create_table(self,cursql):
    #     self.dbcur.execute(cursql)

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

    def insert_resource_center_table(self, par, param):
        fields = ['id', 'type', 'name', 'url', 'link', 'about']

        sqlstr = 'INSERT INTO resource_center('
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['%s' for i in fields])
        sqlstr += ')'

        sql_param = (param['id'], par[1], par[2], par[3],
                     param['link'], param['about'])
        print sql_param
        print sqlstr
        self.dbcur.execute(sqlstr, sql_param)
        self.dbconn.commit()

    def del_tmp_table(self, id):
        self.dbcur.execute("DELETE FROM tmp WHERE id='%s';" % (id))
        self.dbconn.commit()

    def Uniquerows(self):
        pass

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

    def seiri_tmp_table_sql(self, table_name, param):
        fields = ['id', 'type', 'name', 'url']

        sqlstr = 'INSERT INTO %s(' % (table_name)
        sqlstr += ', '.join([item for item in fields])
        sqlstr += ')VALUES('
        sqlstr += ', '.join(['%s' for i in fields])
        sqlstr += ')'

        self.sqlQueue = [
            (sqlstr, (item[0],
                      item[1],
                      item[2],
                      item[3])) for item in param]

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

    def query_tmp_table(self):
        self.dbcur.execute("SELECT * FROM tmp;")
        rows = self.dbcur.fetchall()  # all rows in table
        return rows
