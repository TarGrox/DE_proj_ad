import json
import os

# Third-party
import lxml
from lxml import etree
import requests
# ==========================================

# https://www.lamoda.ru/p/rtlabb019901/clothes-hebymango-dzhinsy/

class Parser():
    def __init__(self):
        #? Ссылку La_link подавать с '/' в конце?
        #? .collect_links, если что, возвращает ссылки с '/' в начале
        self.La_link = 'https://www.lamoda.ru'
        self.xpath_to_collect_links = '//a[@class="x-product-card__link x-product-card__hit-area"]/@href'
        self.xpath_to_collect_js = '//body/script[not(@id) and not(@class) and not(@crossorigin) and not(@type) and not(@src)]'
    
    def collect_links(self, link):
        page = GetHtml.get_html(link)
        links_of_product = page.xpath(self.xpath_to_collect_links)
        print('success')
        return links_of_product
    
    def extract_inf_from_js(self, page):
        # поиск всех <script> без каких-либо тегов
        inf = page.xpath(self.xpath_to_collect_js)
        return inf[0].text
    
    def get_next_link(link):
        #TODO: определить в каком виде получать и передавать дальше ссылку
        pass


class GetHtml():
    def __init__(self):
        pass
    
    #* Обрати внимание, что можно поставить @classmethod, а можно 
    #* добавить (), а конкретнее: GetHtml().get_html(link) - и работать будет
    @classmethod
    def get_html(self, link):
        r = requests.get(link)
        #? Подумать над реализацией, если код != 200, что возвращать?
        print(r.status_code)
        return etree.HTML(r.text) if r.status_code == 200 else None

class CollectReviews():
    def get_reviews(self, link):
        pass    

class Formatter():
    def __init__(self):
        pass
    
    @classmethod
    def from_js_to_dict(self, script):
        mark_product = script.find('"product":{')
        mark_comments_data = script.find('"comments_data":{')
        inf = script[mark_product+len('"product":{')-1:mark_comments_data-1]
        
        return json.loads(inf)

# ========================================
# Обработка страницы продукта:

Pr = Parser()
Gh = GetHtml()
links_of_product = Pr.collect_links('https://www.lamoda.ru/c/517/clothes-muzhskie-bryuki/')
# print(links_of_product)

for link in links_of_product:
    page = Gh.get_html(Pr.La_link + link)
    print(Pr.La_link + link)
    inf = Pr.extract_inf_from_js(page)
    
    