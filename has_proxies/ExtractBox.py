# -*- coding:utf-8 -*-
from BeautifulSoup import BeautifulSoup
from RequestsBox import *
# from PhantomjsBox import *


class ExtractWebFrame:
    url = 'http://www.piaohua.com/html/dongzuo/index.html'
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
    def sortTarget(self, stype, url):
        targetList = []
        page_count = 0
        while 1:
            try:
                tmpUrl = url + 'index.html'
                html = self.resBox.proxyGet(tmpUrl)
                self.resBox.saveHtml(html.content)

                soup = BeautifulSoup(html.content)
                page_count = soup("div", "page tk")[0]
                page_count = int(page_count.strong.string)
            except Exception, ex:
                print ex
            else:
                film = soup.findAll(id='list')[0]
                #film_list = film_list.findAll('strong')

                film_list = []
                for item in film('dl'):
                    dfilm = dict()
                    dfilm['url'] = url + item.a['href']
                    if item('font'):
                        dfilm['name'] = item.font.string
                    elif item('b'):
                        dfilm['name'] = item.b.string
                    elif item('strong'):
                        dfilm['name'] = item.strong.a.string
                    else:
                        dfilm['name'] = item
                    dfilm['type'] = stype
                    dfilm['id'] = self.createDBID()

                    film_list.append(dfilm)

                return page_count, film_list

    def sortTraverseTarget(self, ncount, stype, url):

        nsite = 1
        while 1:
            try:
                for i in xrange(nsite, ncount):
                    nsite = i
                    if i == 1:
                        continue
                    else:
                        tmpUrl = url + 'list_%s.html' % (i)
                    print tmpUrl
                    html = self.resBox.proxyGet(tmpUrl)

                    soup = BeautifulSoup(html.content)
                    film = soup.findAll(id='list')[0]
                    #film_list = film_list.findAll('strong')
                    film_list = []
                    for item in film('dl'):
                        dfilm = dict()
                        dfilm['url'] = url + item.a['href']
                        if item('font'):
                            dfilm['name'] = item.font.string
                        elif item('b'):
                            dfilm['name'] = item.b.string
                        elif item('strong'):
                            dfilm['name'] = item.strong.a.string
                        else:
                            dfilm['name'] = item
                        dfilm['type'] = stype
                        dfilm['id'] = self.createDBID()

                        film_list.append(dfilm)

                    yield film_list

            except Exception, ex:
                print ex
            else:
                break

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
