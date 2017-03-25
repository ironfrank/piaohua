#coding:utf-8
import psycopg2
import time
import random
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def createDBID():
    timestamp = time.time()
    timestamp = '%f' % timestamp
    timestamp = ''.join(timestamp.split('.'))

    random_number = random.uniform(1000, 9999)
    random_number = '%.6f' % random_number
    random_number = ''.join(random_number.split('.'))
    return timestamp + random_number

# 数据库连接参数
conn = psycopg2.connect(database="piaohua", user="frank", password="root", host="127.0.0.1", port="5432")
cur = conn.cursor()
sqlconn = MySQLdb.connect(host='182.254.242.28', user='root', passwd='root', port=3306)
sqlcur = sqlconn.cursor()
sqlconn.select_db('film')


cur.execute("SELECT * FROM piaohua;")
rows = cur.fetchall()        # all rows in table
sql_statement = ''
try:
    for item in rows:
        item_list = list(item)
        del(item_list[-1])
        value = "\",\"".join(list(item_list))
        #print value
        sql_statement = '''INSERT INTO piaohua (id,type,name,url) VALUES ("%s");''' % value
        print sql_statement

        sqlcur.execute(sql_statement)
except Exception,ex:
    print sql_statement



sqlconn.commit()
conn.commit()
cur.close()
conn.close()
sqlcur.close()
sqlconn.close()