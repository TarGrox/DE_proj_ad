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
    
    def parse_page(self, link):
        La_link = self.La_link
        page = GetHtml.get_html(La_link + link)
        raw_inf = ExtractorInfFromJS.extract_inf_from_js(page)
        inf_json =  Formatter.from_js_to_json(raw_inf)
        sku_list = ListOfRelatedProds.collect_list_of_product(inf_json) # sku - уникальные имена сопутствующих товаров со странцы
        attrs = CollectAttrs.collect_prod_attrs(inf_json)
        img_list = CollectImgs.collect_prod_imgs(inf_json)
        name = CollectName.collect_name(inf_json)
        
        return name
    
    def parse_page_related_prods(self, link):
        La_link = self.La_link
        pass


class ExtractorInfFromJS():
    xpath_to_collect_js = '//body/script[not(@id) and not(@class) and not(@crossorigin) and not(@type) and not(@src)]'
    
    @classmethod
    def extract_inf_from_js(cls, page):
        # поиск всех <script> без каких-либо тегов
        # нужный нам <script> первый
        inf = page.xpath(cls.xpath_to_collect_js)
        return inf[0].text
    #TODO: если extract_inf_from_js не найдет нужный <script>,
    #TODO: создать и второй метод, перебирающий все <script> с поиском по контексту


class ListOfRelatedProds():
    
    @classmethod
    def collect_list_of_product(cls, inf_json):
        sku_list = []
        # inf_json -> list of related_product -> get_html each -> extract_inf_from_js 
        for i in inf_json['related_products']:
            sku_list.append(i['sku'])
        return sku_list


class ConrollerOfPrPP():
    def __init__(self):
        pass
    
    def page_processing():
        # 
        pass

class GetHtml():
    
    #* Обрати внимание, что можно поставить @classmethod, а можно 
    #* добавить () {пример: GetHtml().get_html(link)} - и работать будет
    @classmethod
    def get_html(cls, link):
        r = requests.get(link)
        #? Подумать над реализацией, если код != 200, что возвращать?
        print(r.status_code)
        return etree.HTML(r.text) if r.status_code == 200 else None


class CollectReviews():
    def get_reviews(self, link):
        pass    

class CollectAttrs():
    
    # Собирает информацию о составе, материалах и тд
    @classmethod
    def collect_prod_attrs(cls, inf_json):
        attrs = dict()
        for i in inf_json['attributes']:
            key = i['params']['title']
            attrs[key] = i['text']
        
        return attrs

class CollectImgs():
    La_link = 'https://a.lmcdn.ru/img600x866'
    
    @classmethod
    def collect_prod_imgs(cls, inf_json):
        img_list = list()
        
        for i in inf_json['media']['images']:
            img_list.append(cls.La_link + i['src'])
        
        return img_list

class CollectName():
    
    @classmethod
    def collect_name(cls, inf_json):
        
        return inf_json['brand']['model_name']

class Formatter():
    
    @classmethod
    def from_js_to_json(cls, script):
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
# for link in links_of_product:

print(PrPP.parse_page('/p/UN001EMLYPQ2/'))