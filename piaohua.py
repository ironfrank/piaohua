# -*- coding:utf-8 -*-
from ExtractBox import *
from PiaohuaDB import *
import collections
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def UpdateDB(db, exbox, res, main_table=False, film_type=None):
    rows = db.query_tmp_table()
    if (not rows) and main_table:
        db.piaohua_type2tmp_table(film_type)

    rows = db.query_tmp_table()
    for row in rows:
        lrow = [item for item in row]
        print lrow
        status_code, html = res.proxy_get_func(lrow[3])

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

def UpdateFilms(db, exbox, res):
    film_url = 'http://www.piaohua.com'
    old_date = db.query_update_log()
    old_date = old_date[0][0]
    status_code, html = res.proxy_get_func(film_url)
    if status_code == '200':
        film_list = exbox.sort_film_new_links(html, old_date, film_url)
        print film_list
        if isinstance(film_list, list):
            for item in film_list:
                db.single_insert_tmp_table('tmp', item)



def main():
    db = PiaohuaDB('film', '127.0.0.1')
    exbox = ExtractWebFrame()
    res = RequestsBox()

    UpdateFilms(db, exbox, res)
    db.update_log()
    UpdateDB(db, exbox, res, False, '')

if '__main__' == __name__:
    main()
