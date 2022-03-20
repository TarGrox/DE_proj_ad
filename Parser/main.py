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
        self.WorkerInf = WorkerInf()
    
    def parse_page(self, link):
        WorkerInf = self.WorkerInf
        
        inf_json = WorkerInf.output_inf_json(link)
        
        sku_list = CollectSkuOfRelatedProds.collect_tuple_of_product(inf_json) # sku - уникальные имена сопутствующих товаров со страницы
        attrs = CollectAttrs.collect_prod_attrs(inf_json)
        img_tuple = CollectImgs.collect_prod_imgs(inf_json)
        name = CollectName.collect_name(inf_json)
        brand_name = CollectBrandName.collect_name(inf_json)
        price = CollectPrice.collect_price(inf_json)
        size = CollectSize.collect_size(inf_json)
        
        return sku_list, attrs, img_tuple, name, brand_name, price, size
    
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

class WorkerInf():
    """
    Делает запрос, получает информацию, выразает и обрабатывает её
    Возвращает json о продукте
    """
    
    def __init__(self) -> None:
        #? Ссылку La_link подавать с '/' в конце?
        self.La_link = 'https://www.lamoda.ru'
        self.GetResponse = GetResponse()
        self.GetTextFromResponse = GetTextFromResponse()
    
    def output_inf_json(self, link):
        
        # Переименовываем объекты нужных нам классов
        La_link = self.La_link
        GetResponse = self.GetResponse
        GetTextFromResponse = self.GetTextFromResponse
        
        response = GetResponse.get_response(La_link+link)
        page = GetTextFromResponse.response_to_text(response)
        
        raw_inf = ExtractorInfFromJS.extract_inf_from_js(page)
        del page
        inf_json =  Formatter.from_js_to_json(raw_inf)
        del raw_inf
        return inf_json

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
        self.offset = 5
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
        
        # self.work()
        
        # Устанавливаем sku, params, headers, cookies
        self.CFR.set_sku(sku) # обновились headers
        self.CFR.set_params()
        self.CFR.set_cookies( self.GC.get_cookies(sku) )
        
        
        
        # self.collect_inf()
        1+1
        
    def collect_inf(self):
        """
        Непосредственно собирает информацию
        """
        # Rcsdf = GetResponse1()
        # sdf = Rcsdf.get_response('https://www.lamoda.ru/p/un001emlypq1/', self.CFR.headers, self.CFR.params, self.CFR.cookies)
        # sdf1 = Rcsdf.get_response('https://www.lamoda.ru/p/un001emlypq1/', '', '', '')
        # 1+1
        pass
    
    def process(self):
        """
        Именно этот метод будет вызываться
        """
        pass

class GetCookies(GetResponse):
    def __init__(self) -> None:
        super().__init__()
        self.La_link = 'https://www.lamoda.ru/p/'
    
    def get_cookies(self, sku):
        La_link = self.La_link
        response = self.get_response(La_link + sku)
        return response.cookies
    



#! Переписать?
class GetHtmlRelatedProds(GetHtml):
    La_link = 'https://www.lamoda.ru/p'

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
# Обработка страницы продукта:

PrC = ParserCategory()
PrPP = ParserProductPage()
Gh = GetHtml()
# links_of_product = PrC.collect_links('https://www.lamoda.ru/c/517/clothes-muzhskie-bryuki/')
# print(links_of_product)

links_of_product = ['/p/UN001EMLYPQ2/']
# for link in links_of_product:

# print(PrPP.parse_page('/p/UN001EMLYPQ2/'))

# Wc = WorkerAPIComments('UN001EMLYPQ2')
PrPP1 = ParserProductPage()
print(PrPP1.parse_page('/p/UN001EMLYPQ2/'))
1+1
# print(Gh.get_html('https://www.lamoda.ru/api/v1/product/reviews?sku=MP002XM1RJVM&sort=date&sort_direction=desc&offset=10&limit=5&only_with_photos=false'))
