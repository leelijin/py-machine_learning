from bs4 import BeautifulSoup
import urllib.request as url_re


class MyHtml:
    def __init__(self, from_url):
        self.url = from_url

    def get_raw_html(self):
        response = url_re.urlopen(self.url)
        return response.read()

    def get_content(self):
        soup = BeautifulSoup(self.get_raw_html(), 'html5lib')

        item = []
        for node in soup.find_all(class_='sd-box-list'):
            link = node.h2.a['href']
            title = node.h2.a.string
            desc = node.find(class_='text').string
            tags = node.find(class_='key').string
            item.append((link, title, desc, tags))
        return item
