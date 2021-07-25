from bs4 import BeautifulSoup
import requests


class Crawler:
    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.session = requests.Session()

    def crawl(self):
        pass

    def parse(self):
        pass
# https://www.mustgo.com/worldlanguages/languages-a-z/

class GutenbergCrawler(Crawler):
    # Simdi ilk once bizim sectigimiz yazar listesine bakacak idsini verecegiz
    #  id'den yazarin kitap linklerini tiklayacak
    #  ararken kelielerin icinde german vs geciyorsa onlari atlayacak
    #  burada dile gore filtreleme  (lowercase check etme)
    #  kitaplara girdiginde orada da utf8'i linkini bulup
    #  txt dosyasini kaydedecek (author-book-name)


    pass



