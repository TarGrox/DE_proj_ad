from abc import abstractmethod
import json
import os
import cProfile

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
        
        self.ProcessPageToText = ProcessPageToText()
    
    def collect_links(self, link):
        
        ProcessPageToText = self.ProcessPageToText
        
        page = ProcessPageToText.output_inf_in_text(link)
        
        links_of_product = page.xpath(self.xpath_to_collect_links)
        print('success')
        
        return links_of_product
    
    def get_next_link(self, page):
        #TODO: определить в каком виде получать и передавать дальше ссылку
        # return link_to_next_page
        pass

class ParserProductPage():
    def __init__(self):
        self.ProcessPageToText = ProcessPageToText()
        self.ProcessInf = ProcessInf()
        self.sku_tuple = ()
        self.La_link = 'https://www.lamoda.ru'

    
    def parse_page(self, link):
        ProcessPageToText = self.ProcessPageToText
        La_link = self.La_link
        
        page = ProcessPageToText.output_inf_in_text(La_link + link)
        raw_inf = ExtractorInfFromJS.extract_inf_from_js(page)
        del page
        
        inf_json =  Formatter.from_js_to_json(raw_inf)
        del raw_inf
        
        
        sku_tuple = CollectSkuOfRelatedProds.collect_tuple_of_product(inf_json) # sku - уникальные имена сопутствующих товаров со страницы
        attrs = CollectAttrs.collect_prod_attrs(inf_json)
        img_tuple = CollectImgs.collect_prod_imgs(inf_json)
        name = CollectName.collect_name(inf_json)
        brand_name = CollectBrandName.collect_name(inf_json)
        price = CollectPrice.collect_price(inf_json)
        size = CollectSize.collect_size(inf_json)
        
        #TODO: объявить эту переменную
        self.sku_tuple = sku_tuple
        
        print(name, brand_name, price, attrs, img_tuple, size, sku_tuple, sep='\n')
        
        return sku_tuple, attrs, img_tuple, name, brand_name, price, size
    
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


class CollectSkuOfRelatedProds():
    """Собирает sku (уникальные идентификаторы - почти ссылки) сопутствующих товаров с нынешней страницы
    продукта
    Возвращает tuple"""
    
    @classmethod
    def collect_tuple_of_product(cls, inf_json):
        sku_list = []
        # inf_json -> list of related_product -> get_html each -> extract_inf_from_js
        for i in inf_json['related_products']:
            sku_list.append(i['sku'])
        return tuple(sku_list)

class ProcessPageToText():
    """
    Делает запрос, получает информацию, выразает и обрабатывает её
    Возвращает text о продукте
    """
    
    def __init__(self) -> None:
        #? Ссылку La_link подавать с '/' в конце?
        self.La_link = 'https://www.lamoda.ru'
        self.GetResponse = GetResponse()
        self.GetTextFromResponse = GetTextFromResponse()
    
    def output_inf_in_text(self, link):
        
        # Переименовываем объекты нужных нам классов
        La_link = self.La_link
        GetResponse = self.GetResponse
        GetTextFromResponse = self.GetTextFromResponse
        
        response = GetResponse.get_response(link)
        page = GetTextFromResponse.response_to_text(response)
        return page

class ProcessPageToJson():
    """
    Делает запрос, получает информацию, выразает и обрабатывает её
    Возвращает text о продукте
    """
    
    def __init__(self) -> None:
        #? Ссылку La_link подавать с '/' в конце?
        self.La_link = 'https://www.lamoda.ru'
        self.GetResponse = GetResponse()
    
    def output_inf_in_json(self, link, headers='', params='', cookies=''):
        
        # Переименовываем объекты нужных нам классов
        La_link = self.La_link
        GetResponse = self.GetResponse
        
        response = GetResponse.get_response(link, headers, params, cookies)
        page = GetJsonFromResponse.response_to_json(response)
        return page


class ProcessInf():
    def __init__(self) -> None:
        self.ContainerInfProd = ContainerInfProd()
    
    def process_inf(self, inf_json):
        """
        sku_list;
        attrs;
        img_tuple;
        name;
        brand_name;
        price;
        size;
        """
        
        sku_list = CollectSkuOfRelatedProds.collect_tuple_of_product(inf_json) # sku - уникальные имена сопутствующих товаров со страницы
        attrs = CollectAttrs.collect_prod_attrs(inf_json)
        img_tuple = CollectImgs.collect_prod_imgs(inf_json)
        name = CollectName.collect_name(inf_json)
        brand_name = CollectBrandName.collect_name(inf_json)
        price = CollectPrice.collect_price(inf_json)
        size = CollectSize.collect_size(inf_json)

class ContainerInfProd():
    def __init__(self) -> None:
        pass


class GetResponse():
    def __init__(self) -> None:
        self.ResponseHendler = ResponseHendler_GetResponse()
    
    def get_response(self, link, headers='', params='', cookies=''):
        response = requests.get(link, headers=headers, params=params, cookies=cookies)
        self.ResponseHendler.process_result(response)
        
        return response

class ResultHendlerScheme():
    """Обрабатывает результат работы класса и/или метода"""
    #TODO: Добавить метод, получающий название и путь до файла логирования
    
    @abstractmethod
    def process_result(self, obj_to_process) -> None:
        pass
    pass

class ResponseHendler_GetResponse(ResultHendlerScheme):
    """Обрабатывает ответ от GetResponse()
    Если r.status_code != 200, то логировать в файл"""
    
    def process_result(self, response):
        #TODO: Дописать логирование в файл
        if response.status_code != 200:
            print(response.status_code, response.reason)
        else:
            #! Переписать, здесь нужно записывать лог
            print(response.status_code, response.reason)



class GetTextFromResponse():
    
    @staticmethod
    def response_to_text(response):
        return etree.HTML(response.text)

class GetJsonFromResponse():
    
    @staticmethod
    def response_to_json(response):
        return response.json()


class ContainerForRequest():
    """Устанавливает и хранит cookies, params, headers
    На вход нужно подать sku, offset
    Порядок инициализации: sku, offset, cookies"""
    
    def __init__(self):
        self.offset = 0
        self.sku = 'none'
        self.cookies = []
        self.set_headers()
        self.set_params()
        
    
    def set_sku(self, sku):
        """
        Обновляет sku и headers
        Sku example: UN001EMLYPQ1
        """
        self.sku = sku
        self.set_headers()
    
    def set_cookies(self, cookies):
        self.cookies = cookies
        1+1
    
    # меняется только sku
    def set_headers(self):
        referer_link = 'https://www.lamoda.ru/p/' + self.sku + '/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Referer': referer_link,
            'Connection': 'keep-alive',
        }
    
    # меняется и sku, и offset
    def set_params(self):
        self.params = (
            ('sku', self.sku),
            ('sort', 'date'),
            ('sort_direction', 'desc'),
            ('offset', self.offset),
            ('limit', '5'),
            ('only_with_photos', 'false'),
        )
    
    def move_offset(self):
        self.offset += 5
        self.set_params()


# Для работы с API/comments мне нужно:
# 1. GetResponse()
#   1.1 для получения первичных coockie при создании;
#   1.2 для непосредственной работы с API;
# 2. ContainerForRequest():
#   2.1 Продумать как менять offset
# 3. GetJsonFromResponse():
#   3.1 для перевода из response в json;
# 4. Непосредственная работа с json:
#   4.1 вытаскиваем дату-время, коммент, имя, оценку
# 5. Куда и как передавать данные?

class WorkerAPIComments():
    def __init__(self, sku) -> None:
        self.GR = GetResponse()
        self.CFR = ContainerForRequest()
        self.GJFR = GetJsonFromResponse()
        self.GC = GetCookies()
        self.ProcessPageToJson = ProcessPageToJson()
        
        
        # Устанавливаем sku, params, headers, cookies
        self.CFR.set_sku(sku) # обновились headers
        self.CFR.set_params()
        self.CFR.set_cookies( self.GC.get_cookies(sku) )
        
        #
        self.api_link = 'https://www.lamoda.ru/api/v1/product/reviews'
        self.total_num = self.process()['total']
        
        if self.total_num == 0:
            return
        self.loop()
        
        print('hello')
    
    def process(self):
        
        r_json = self.ProcessPageToJson.output_inf_in_json(self.api_link, headers=self.CFR.headers,\
            params=self.CFR.params,\
                cookies=self.CFR.cookies)
        # print(r_json['reviews'])
        return r_json
    
    def loop(self):
        
        for i in range( (self.total_num // 5) + 1  ):
            r_json = self.process()
            
            self.export(r_json)
            
            self.CFR.move_offset()
    
    def export(self, r_json):
        # print(len(r_json['reviews']))
        # print(r_json['reviews'])
        
        pass

class GetCookies(GetResponse):
    def __init__(self) -> None:
        super().__init__()
        self.La_link = 'https://www.lamoda.ru/p/'
    
    def get_cookies(self, sku):
        La_link = self.La_link
        response = self.get_response(La_link + sku)
        return response.cookies
    

class CollectReviews():
    # url = 'https://www.lamoda.ru/api/v1/product/reviews?sku=rtlabe015303&sort=date&sort_direction=desc'
    
    def get_reviews(self, link):
        pass
    
    def get_total_numb_reviwes(self, link):
        url = self.api_link + link + self.sort_settings

class CollectAttrs():
    """Собирает информацию о составе, материалах и тд - просто передать inf_json"""
    
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
        
        return tuple(img_list)

class CollectNameScheme():

    @classmethod
    def collect_name(cls, inf_json):
        return inf_json['brand'][cls.name_type]

class CollectName(CollectNameScheme):
    name_type = 'model_name'
class CollectBrandName(CollectNameScheme):
    name_type = 'name'

class CollectPrice():
    """Собирает цену продукта - full_price и price_w/_sale в виде tuple.
    if sale:
        ( full_price, price_w_sale )
    else:
        ( full_price, None )"""
    
    @classmethod
    def collect_price(cls, inf_json):
        """определяет, продается товар со скидкой или нет
        если да, собирать две цены, делать из них кортеж"""
        types_of_price = cls.get_len(inf_json)
        if types_of_price == 1:
            return ( CollectPriceWoSale.collect_price(inf_json), None )
        if types_of_price == 2:
            return ( CollectPriceWoSale.collect_price(inf_json), CollectPriceWSale.collect_price(inf_json) )
        else:
            #TODO: Создать обработчик, если цена не указана
            print(f'Some error in {cls}')
        
    @staticmethod
    def get_len(inf_json):
        return len(inf_json['detailed_price']['details'])
    

class CollectPriceScheme():
    
    @classmethod
    def collect_price(cls, inf_json):
        return inf_json['detailed_price']['details'][cls.i]['value']

class CollectPriceWoSale(CollectPriceScheme):
    i = 0

class CollectPriceWSale(CollectPriceScheme):
    i = 1

class CollectSize():
    """Перебирает все sizes по нужным ключам, возвращает dict вида:
    {0: {'is_available': True, 'brand_size': 'S', 'size': '46/48'}, 1: {'is_available': True,..."""
    
    right_keys = ['is_available','brand_size','size']
    
    #TODO: определить как выводить информацию
    @classmethod
    def collect_size(cls, inf_json):
        right_keys = cls.right_keys
        
        out = {}
        for pos, sizes in enumerate(inf_json['sizes']):
            keys = sizes.keys() and right_keys
            out[pos] = {}
            for key in keys:
                out[pos][key] = sizes[key]
        
        return out

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

sku_1 = 'mp002xm1k3hy'.upper()
WAPI = WorkerAPIComments(sku_1)
WAPI.process()

print('hello')
print('hello')
ParserCategory_obj = ParserCategory()
link = 'sdf' #TODO: перенести эту строку вконец
link = 'https://www.lamoda.ru/c/477/'
links = ParserCategory_obj.collect_links(link)
# next_link = ParserCategory_obj.get_next_link(link) #TODO: дописать этот метод

del ParserCategory_obj
for link in links:
    ParserProductPage_origin = ParserProductPage()
    ParserProductPage_origin.parse_page(link)
    
    sku_rel_prods = ParserProductPage_origin.sku_tuple
    
    del ParserProductPage_origin
    for sku in sku_rel_prods:
        line = '=============' 
        print(line, line, line, line, line, sep='\n')
        ParserProductPage_related = ParserProductPage()
        link_rel_prods = '/p/' + sku
        ParserProductPage_related.parse_page(link_rel_prods)
        print(line, line, line, line, line, sep='\n')
        
        del ParserProductPage_related
        pass