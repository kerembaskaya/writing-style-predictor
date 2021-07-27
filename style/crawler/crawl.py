# from bs4 import BeautifulSoup
from abc import abstractmethod

import requests

from utils.world_languages import get_languages


class DataWrangler:
    def __init__(self, baseurl):
        self.baseurl = baseurl
        self.session = requests.Session()

    @abstractmethod
    def crawl(self):
        raise NotImplementedError

    @abstractmethod
    def parse(self):
        raise NotImplementedError


class GutenbergWrangler(DataWrangler):
    # Simdi ilk once bizim sectigimiz yazar listesine bakacak idsini verecegiz
    #  id'den yazarin kitap linklerini tiklayacak
    #  ararken kelielerin icinde german vs geciyorsa onlari atlayacak
    #  burada dile gore filtreleme  (lowercase check etme)
    #  kitaplara girdiginde orada da utf8'i linkini bulup
    #  txt dosyasini kaydedecek (author-book-name)
    pass


def run():
    languages = get_languages()
    print(languages)


if __name__ == "__main":
    run()
