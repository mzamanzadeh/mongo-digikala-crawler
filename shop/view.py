from django.shortcuts import render

from shop.mongo import db_helper


def category(request,category_name):

    filters = {}

    from_price = request.GET.get("from-price",None)
    if from_price:
        filters['price'] = {'$gte': int(from_price)}

    to_price = request.GET.get("to-price",None)
    if to_price:
        filters['price']['$lte'] = int(to_price)



    helper = db_helper()
    db = helper.getDB()
    products = db['category-'+category_name].find(filters)
    maxPrice = db['category-'+category_name].find_one(sort = [('price',-1)])
    categories = db.categories.find()
    return render(request,'category.html',{'products': products,'categories': categories,'maxPrice': maxPrice['price']})

def product(request, product_id):
    helper = db_helper()
    db = helper.getDB()
    categoryName = db.products.find_one({'product_id': product_id})
    product = db[categoryName['category']].find_one({'product_id': product_id})
    return render(request,'product.html',{'product': product})