# -*- coding:utf-8 -*-
from ExtractBox import *
from PiaohuaDB import *
import collections


def UpdateDB():
    db = PiaohuaDB('test', '127.0.0.1')
    exbox = ExtractWebFrame()
    res = RequestsBox()
    rows = db.query_tmp_table()
    if not rows:
        db.piaohua_type2tmp_table('aiqing')

    rows = db.query_tmp_table()
    for row in rows:
        lrow = [item.encode('utf-8') for item in row]
        print lrow[0], lrow[1], lrow[2], lrow[3]
        status_code, html = res.proxy_get_func(lrow)

        if status_code == '200':
            film_dict = exbox.sort_film_links(html)
            if isinstance(film_dict, dict):
                db.insert_resource_center_table(lrow, film_dict)
            else:
                db.single_insert_tmp_table('tmp_unresolved_issues', lrow)
                
            db.del_row_from_id_table('tmp', lrow[0])
        elif status_code == '404':
            db.single_insert_tmp_table('tmp_404', lrow)
            db.del_row_from_id_table('tmp', lrow[0])

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
