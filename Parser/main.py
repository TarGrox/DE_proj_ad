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
    
    def collect_links(self, link):
        page = RequestsClass.get_html(link)
        links_of_product = page.xpath(self.xpath_to_collect_links)
        print('success')
        
        return links_of_product
    
    def extract_inf_from_js(self, link):
        pass
    
    def get_next_link(link):
        #TODO: определить в каком виде получать и передавать дальше ссылку
        pass


class RequestsClass():
    def get_html(link):
        r = requests.get(link)
        #? Подумать над реализацией, если код != 200, что возвращать?
        print(r.status_code)
        return etree.HTML(r.text) if r.status_code == 200 else None
    
    def collect_reviews(link):
        pass

# ========================================
# Обработка страницы продукта:

Pr = Parser()
Rc = RequestsClass()
links_of_product = Pr.collect_links('https://www.lamoda.ru/c/517/clothes-muzhskie-bryuki/')
print(links_of_product)


for link in links_of_product:
    # page = Rc.get_html(link)
    print(Pr.La_link + link)
    