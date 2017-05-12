#coding:utf-8
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 数据库连接参数
conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', port=3306)
cur = conn.cursor()
conn.select_db('film')


cur.execute("SELECT id,name,about FROM resource_center;")
rows = cur.fetchall()        # all rows in table
sql_statement = ''
#print len(rows)

for item in rows:
    about = item[2].replace('&nbsp;','')
    about = about.replace('　','')
    duration = re.findall('◎年代(.*?)◎', about, re.S)
    country = re.findall('◎国家(.*?)◎', about, re.S)
    classify = re.findall('◎类别(.*?)◎', about, re.S)
    imdb = re.findall('◎IMDB评分(.*?)◎', about, re.S)

    duration = duration[0] if duration else ''
    country = country[0] if country else ''
    classify = classify[0] if classify else ''
    imdb = imdb[0] if imdb else ''

    execute_sql = '''UPDATE resource_center SET duration="%s" , country="%s", classify="%s", imdb="%s" WHERE id="%s";''' %(duration, country, classify, imdb, item[0])

    #execute_sql = '''UPDATE resource_center SET update_date="2017-03-23" WHERE id="%s";''' % item[0]
    cur.execute(execute_sql)
    conn.commit()

# id = ''
# try:
#     for index, item in enumerate(rows):
#         item_list = list(item)
#         item_list[2] = item_list[2].replace('"', '&quot;')
#         #cur.execute("UPDATE piaohua SET name = '%s' WHERE ID = '%s';" % (item_list[2], item_list[0]))
#
#         id = item_list
#         value = "\",\"".join(list(item_list))
#         sql_statement = '''INSERT INTO piaohua (id,type,name,url) VALUES ("%s");''' % value
#
#         print """\033[1;31;40m %s \033[0m""" % (index)
#         cur.execute(sql_statement)
#         conn.commit()
# except Exception,ex:
#     print ex
#     print sql_statement
#     print id

cur.close()
conn.close()
