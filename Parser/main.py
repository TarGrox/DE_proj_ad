import json
import os

# Third-party
import lxml
from lxml import etree
import requests
# ==========================================

# https://www.lamoda.ru/c/513/clothes-muzhskie-d-insy/?sitelink=topmenuM&l=7

# сделать async/await -> подавать кусками в Парсер через трансформацию в file-like object
r = requests.get('https://www.lamoda.ru/c/513/clothes-muzhskie-d-insy/')
print(r.status_code)

rewrite_flag = False
if (r.status_code == 200) and (rewrite_flag == True):
    namefile = 'myfile.html'
    f = open(namefile, 'w')
    f.write(r.text)
    print(f'file {namefile} has been overwritten')

html_etree = etree.HTML(r.text)
links_of_product = html_etree.xpath('//a[@class="x-product-card__link x-product-card__hit-area"]/@href')

print(len(links_of_product))
print(links_of_product)

# ========================================
# Обработка страницы продукта:

for link in links_of_product:
    # r = requests.get('https://www.lamoda.ru' + link)
    print('https://www.lamoda.ru' + link)