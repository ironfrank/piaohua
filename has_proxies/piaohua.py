# -*- coding:utf-8 -*-
from ExtractBox import *
from PiaohuaDB import *
import collections


def UpdateDB():
    db = PiaohuaDB()
    exbox = ExtractWebFrame()
    res = RequestsBox()
    #file_dict = collections.defaultdict(str)
    # film_dict = dict()
    # as_dict = dict()
    # #去除重复
    # rows = db.QueryPiaohuaTable()
    # n = 0
    # for item in rows:
    #     tmpurl = item[3].split('/')
    #     for i in xrange(3):
    #         del tmpurl[5]

    #     print tmpurl
    #     print '/'.join(tmpurl)
    #     db.UpdatePiaohuaTable(item[0],'/'.join(tmpurl))
    # print n

    #rows = db.query_type_table('dongzuo')
    #db.seiri_tmp_table_sql('tmp', rows)
    # db.execute_sql()
    rows = db.query_tmp_table()
    for row in rows:
        print row[0], row[1], row[2], row[3]
        status_code, html = res.proxy_get(row)

        if status_code == '200':
            film_dict = exbox.sort_film_links(html)
            if isinstance(film_dict, dict):
                db.insert_resource_center_table(row, film_dict)
            else:
                db.seiri_tmp_table_sql('unresolved_issues', [row])
                db.execute_sql()
            db.del_tmp_table(row[0])
        elif status_code == '404':
            db.seiri_tmp_table_sql('piaohua_404', [row])
            db.execute_sql()
            db.del_tmp_table(row[0])

    # type_list = ['kehuan','juqing','xuannian','wenyi','zhanzheng','kongbu','zainan','lianxuju','dongman','zongyijiemu']
    # for stype in type_list:
    #     #stype = 'xiju'
    #     url = 'http://www.piaohua.com/html/%s/' %(stype)

    #     page_count, film_list = exbox.sortTarget(stype, url)
    #     db.seiriTargetTableSQL(film_list)
    #     db.executeSQL()

    #     for item in exbox.sortTraverseTarget(page_count, stype, url):
    #         db.seiriTargetTableSQL(item)
    #         db.executeSQL()
    #     #break


def main():
    UpdateDB()


if '__main__' == __name__:
    main()
