from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import re
from shop.mongo import db_helper


def category(request,category_name):

    filters = {}

    keyword = request.GET.get("q",None)
    if keyword:
        reg=re.compile(".*"+keyword+".*",re.IGNORECASE)
        # filters['$or'] = [{'farsi_title':{'$regex': "/.*"+keyword+".*/i"}}, {'en_title': {'$regex': "/.*"+keyword+".*/i"}}]
        filters['$or'] = [{'farsi_title':{'$regex': reg}}, {'en_title': {'$regex': reg}}]
        # filters['$text'] = {'$search': keyword}
        # filters['farsi_title'] = {'$regex': ".*"+keyword+".*"}

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
    return render(request,'category.html',{'products': products,'categories': helper.getCategories(),'maxPrice': maxPrice['price']})

def product_edit(request,product_id):
    helper = db_helper()
    db = helper.getDB()
    categoryName = db.products.find_one({'product_id': product_id})
    product = db[categoryName['category']].find_one({'product_id': product_id})

    if request.method=="POST":
        db[categoryName['category']].update_one({'product_id': product_id},{'$set': {'farsi_title': request.POST['farsi_title'],'en_title': request.POST['en_title'],'price': int(request.POST['price'])}})
        return redirect('/product/'+product_id)
    return render(request, 'product_edit.html', {'product': product})

def product(request, product_id):
    helper = db_helper()
    db = helper.getDB()
    categoryName = db.products.find_one({'product_id': product_id})
    product = db[categoryName['category']].find_one({'product_id': product_id})
    return render(request,'product.html',{'product': product,'categories': helper.getCategories()})

def product_del(request , product_id):

    helper = db_helper()
    db = helper.getDB()
    categoryName = db.products.find_one({'product_id': product_id})
    product = db[categoryName['category']].find_one({'product_id': product_id})
    if request.method=="POST":
        db[categoryName['category']].remove({'product_id': product_id})
        db.products.remove({'product_id': product_id})
        return redirect('/category/'+categoryName['category'][9:])
    return render(request, 'product_del.html', {'product': product})
@csrf_exempt
def add_comment(request, product_id):

    helper = db_helper()
    db = helper.getDB()
    categoryName = db.products.find_one({'product_id': product_id})
    if request.method=="POST":
        comment = {'content':request.POST.get('comment')}
        comment['by'] = "توسط "+request.POST.get('by','ناشناس')
        db[categoryName['category']].update_one({'product_id': product_id},{'$addToSet':{'comments': comment}})
        # db.products.remove({'product_id': product_id})
    return redirect('/product/'+product_id)

def remove_comment(request, product_id,comment_id):

    helper = db_helper()
    db = helper.getDB()
    categoryName = db.products.find_one({'product_id': product_id})

    db[categoryName['category']].update_one({'product_id': product_id},{'$pull': {'comments':{'id': int(comment_id)}}})
        # db.products.remove({'product_id': product_id})
    return redirect('/product/'+product_id)



