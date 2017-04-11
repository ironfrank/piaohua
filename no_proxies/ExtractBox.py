# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
from RequestsBox import *
import datetime
# from PhantomjsBox import *


class ExtractWebFrame:
    url = 'http://www.piaohua.com'
    resBox = None

    def __init__(self):
        self.resBox = RequestsBox()

    @methodName
    def createDBID(self):
        timestamp = time.time()
        timestamp = '%f' % timestamp
        timestamp = ''.join(timestamp.split('.'))

        random_number = random.uniform(1000, 9999)
        random_number = '%.6f' % random_number
        random_number = ''.join(random_number.split('.'))
        return timestamp + random_number

    @methodName
    def createMD5(self, src):
        md = hashlib.md5()
        md.update(src.encode('utf-8'))
        return md.hexdigest()

    @methodName
    def set_url(self, url):
        self.url = url

    @methodName
    def now_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @methodName
    def sort_film_links(self, html):
        try:
            soup = BeautifulSoup(html.content)
            div = soup.findAll('div', id='showinfo')[0]
            about = div.text
            href_list = []  # [item.a['href'] for item in div('table')]
            # for item in div('table'):
            #     if item.a:
            #         href_list.append(item.a['href'])
            for item in div('table'):
                for href in item('a'):
                    href_list.append(href.text)

            href = '|'.join(href_list)
        except Exception, ex:
            return 'Bad'
        else:
            return {'id': self.createDBID(), 'about': about, 'link': href}

    @methodName
    def sort_film_new_links(self, html, cmp_date, www_url):
        try:
            soup = BeautifulSoup(html.content)
            div = soup.findAll('div', id='iml1')[0]

            film_list = []
            for item in div.ul('li'):
                film_url = www_url + item.a['href']
                film_name = item.strong.text
                film_type = film_url.split('/')[2]
                film_date = item.span.text
                film_date = film_date.split('-')

                year, month, day = int(film_date[0]), int(film_date[1]), int(film_date[2])
                film_date = datetime.date(year, month, day)
                print 'cmp',cmp_date,type(cmp_date)
                #cmp_date = cmp_date.split('-')
                #print cmp_date
                #year, month, day = int(cmp_date[0]), int(cmp_date[1]), int(cmp_date[2])
                #print year, month, day
                #cmp_date = datetime.date(year, month, day)
                #print cmp_date
                if film_date > cmp_date:
                    #{'id': self.createDBID(), 'name': film_name, 'type': film_type, 'url': www_url + film_url}
                    film_list.append([self.createDBID(), film_type, film_name, film_url])

        except Exception, ex:
            return 'Bad'
        else:
            return film_list