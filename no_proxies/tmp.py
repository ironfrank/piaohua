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
print len(rows)

id = ''
try:
    for index, item in enumerate(rows):
        item_list = list(item)
        item_list[2] = item_list[2].replace('"', '&quot;')
        #cur.execute("UPDATE piaohua SET name = '%s' WHERE ID = '%s';" % (item_list[2], item_list[0]))

        id = item_list
        value = "\",\"".join(list(item_list))
        sql_statement = '''INSERT INTO piaohua (id,type,name,url) VALUES ("%s");''' % value

        print """\033[1;31;40m %s \033[0m""" % (index)
        sqlcur.execute(sql_statement)
        sqlconn.commit()
except Exception,ex:
    print ex
    print sql_statement
    print id

cur.close()
conn.close()
sqlcur.close()
sqlconn.close()