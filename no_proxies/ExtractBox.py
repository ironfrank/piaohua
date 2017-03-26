# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
from RequestsBox import *
# from PhantomjsBox import *


class ExtractWebFrame:
    url = ''
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
    def setUrl(self, url):
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
            href_list = [item.a['href'] for item in div('table')]
            href = '|'.join(href_list)
        except Exception, ex:
            return 'Bad'
        else:
            return {'id': self.createDBID(), 'about': about, 'link': href}
