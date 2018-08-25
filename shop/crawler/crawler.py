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
    return int(_multiple_replace(mapping, fa).replace(",",""))
#from https://github.com/itmard/Persian/blob/master/persian/persian.py
def _multiple_replace(mapping, text):
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))


def crawl_category(category_name,page=1):
    url = get_category_url(category_name,page)

    html = urlopen(url).read()

    parsed_html = BeautifulSoup(html,'html.parser')

    products = parsed_html.body.find_all('div', attrs={'class':'c-product-box'})
    db = db_helper()
    for product in products:

        if db.getDB()[category_name].find({'product_id': product.get("data-id")}).count()>0:
            if db.getDB()['products'].find({'product_id': product.get("data-id")}).count()==0:
                db.insert_one('products', {'category': 'category-'+category_name,'product_id': product.get("data-id")})
            continue
        product_url = "https://www.digikala.com"+product.find("div",attrs={'class': 'c-product-box__title'}).find("a").get("href")

        data = {}
        data['product_url'] = product_url
        data['product_id'] = product.get("data-id")
        data['farsi_title'] = product.get("data-title-fa")
        data['en_title'] = product.get("data-title-en")
        data['price'] = price_fa2en(product.get("data-price"))
        data['image_url'] = product.find("img").get("src")
        data['comments'] = crawl_comments(data['product_id'])
        data['questions'] = crawl_questions(data['product_id'])
        # print(str(data))
        db.insert_one('category-'+category_name, data)
        db.insert_one('products', {'category': 'category-'+category_name,'product_id':data['product_id']})

    db.getDB()['category-'+category_name].createIndex( { 'farsi_title': "text" } )
    # db.getDB()['category-'+category_name].createIndex( { 'en_title': "text" } )

def crawl_comments(id):
    url = "https://www.digikala.com/ajax/product/comments/"+id+"/?page=1&mode=newest"
    # print(url)
    html = urlopen(url).read()
    parsed_html = BeautifulSoup(html,'html.parser')

    comments = []
    commentsSection = parsed_html.find_all('li')
    for comment in commentsSection:
        if comment.find('p') is not None:

            comments.append({
                'by': comment.find("div",attrs={'class': 'header'}).find("span").contents[0],
                'content': comment.find('p').contents[0]
            })

    return comments

def crawl_questions(id):
    url = "https://www.digikala.com/ajax/product/questions/"+id+"/?page=1&mode=newest"
    # print(url)
    html = urlopen(url).read()
    parsed_html = BeautifulSoup(html,'html.parser')

    questions = []
    questionsSection = parsed_html.find_all('ul',attrs= {'class': 'c-faq__list'})
    for li in questionsSection:
        question = li.find('li',attrs = {'class': 'is-question'})
        questionAnswers = []
        if question is not None:
            for s in question.find_all('p'):
                qa = {'question': {'by': question.find('span').contents[0],'content': str(s)}, 'answers': []}

            answers = li.find_all('li',attrs = {'class': 'is-answer'})
            for answer in answers:
                a = None
                if answer.get('id')!="answerFormItem":
                    for s in answer.find_all('p'):
                        a = s
                    qa['answers'].append({ 'by': answer.find('span').contents[0],'content': str(a) })
            questionAnswers.append(qa)
        questions.append(questionAnswers)
    return questions
