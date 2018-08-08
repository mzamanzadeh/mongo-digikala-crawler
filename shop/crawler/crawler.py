from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from shop.mongo import db_helper


def get_category_url(category_name,page=1):
    # return "http://localhost/view-source_https___www.digikala.com_search_category-electronic-devices__has_selling_stock=1&pageno=2&sortby=7.html"
    return "https://www.digikala.com/search/category-"+category_name+"/?has_selling_stock=1&sortby=7&pageno="+str(page)

def price_fa2en(fa):
    mapping = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
        '.': '.',
    }
    return _multiple_replace(mapping, fa).replace(",","")
#from https://github.com/itmard/Persian/blob/master/persian/persian.py
def _multiple_replace(mapping, text):
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))


def crawl_category(category_name,page=1):
    url = get_category_url(category_name)

    html = urlopen(url).read()

    parsed_html = BeautifulSoup(html,'html.parser')
    products = parsed_html.body.find_all('div', attrs={'class':'c-product-box'})
    db = db_helper()
    for product in products:
        data = {}
        data['product_id'] = product.get("data-id")
        data['farsi_title'] = product.get("data-title-fa")
        data['en_title'] = product.get("data-title-en")
        data['price'] = price_fa2en(product.get("data-price"))
        data['image_url'] = product.find("img").get("src")
        data['product_url'] = product.find("div",attrs={'class': 'c-product-box__title'}).find("a").get("href")
        data['category_slug'] = category_name
        db.insert_one('products', data)

