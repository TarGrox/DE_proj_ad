from base64 import encode
import json
import os

# Third-party
import lxml
from lxml import etree
import requests
# ==========================================

# https://www.lamoda.ru/p/rtlabb019901/clothes-hebymango-dzhinsy/

class ParserCategory():
    def __init__(self):
        #? .collect_links, если что, возвращает ссылки с '/' в начале
        self.La_link = 'https://www.lamoda.ru'
        self.xpath_to_collect_links = '//a[@class="x-product-card__link x-product-card__hit-area"]/@href'
    
    def collect_links(self, link):
        page = GetHtml.get_html(link)
        links_of_product = page.xpath(self.xpath_to_collect_links)
        print('success')
        return links_of_product
    
    def get_next_link(link):
        #TODO: определить в каком виде получать и передавать дальше ссылку
        pass


class ParserProductPage():
    def __init__(self):
        #? Ссылку La_link подавать с '/' в конце?
        self.La_link = 'https://www.lamoda.ru'
        self.xpath_to_collect_js = '//body/script[not(@id) and not(@class) and not(@crossorigin) and not(@type) and not(@src)]'
    
    def extract_inf_from_js(self, page):
        # поиск всех <script> без каких-либо тегов
        # нужный нам <script> первый
        inf = page.xpath(self.xpath_to_collect_js)
        return inf[0].text
    
    def get_another_product():
        pass


class GetHtml():
    def __init__(self):
        pass
    
    #* Обрати внимание, что можно поставить @classmethod, а можно 
    #* добавить () {пример: GetHtml().get_html(link)} - и работать будет
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
    def from_js_to_json(self, script):
        #* необходимо привести JS <script> к удобоваримому виду - если выкинуть явные куски JS кода,
        #* то можно преобразовать оставшееся в json без ошибок.
        #* Работаем с <script> как с текстом, находим нужный кусок информации через .find - он содержит вид dict.
        #* Оставляем только непосредственную информацию по продукту - размер, цвет и тд.
        
        mark_product = script.find('"product":{')
        mark_comments_data = script.find('"comments_data":{')
        inf = script[mark_product+len('"product":{')-1:mark_comments_data-1]
        
        return json.loads(inf)


# ========================================
# Обработка страницы продукта:

PrC = ParserCategory()
PrPP = ParserProductPage()
Gh = GetHtml()
# links_of_product = PrC.collect_links('https://www.lamoda.ru/c/517/clothes-muzhskie-bryuki/')
# print(links_of_product)

links_of_product = ['/p/UN001EMLYPQ2/']
for link in links_of_product:
    page = Gh.get_html(PrPP.La_link + link)
    print(PrPP.La_link + link)
    raw_inf = PrPP.extract_inf_from_js(page)
    
    inf_json =  Formatter.from_js_to_json(raw_inf)
    print(inf_json['related_products'])
    # print(inf_json)
    # прямо сейчас необходимо собрать все дополнительные варианты с одной странице.
    # некоторые страницы хранят два варианта расцветки, например
    
    sku_list = []
    # inf_json -> list of related_product -> get_html each -> extract_inf_from_js 
    print(inf_json['related_products'][0]['sku']) # для вывода одного сопутствующего товара
    for i in inf_json['related_products']:
        sku_list.append(i['sku'])
    print(sku_list)
    #TODO: вытащить все сопутствующие товары из нынешний страницы
    #TODO: пройтись по ним
    
    1+1