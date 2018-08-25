"""digikalaMongo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from shop.crawler.importer import importer
import shop.view as views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^category/(?P<category_name>.+)/$', views.category),
    url(r'^product/(?P<product_id>\d+)/edit$', views.product_edit),
    url(r'^product/(?P<product_id>\d+)/remove$', views.product_del),
    url(r'^product/(?P<product_id>\d+)/comment$', views.add_comment),
    url(r'^product/(?P<product_id>\d+)/delcom/(?P<comment_id>\d+)', views.add_comment),
    url(r'^product/(?P<product_id>\d+)/$', views.product),
]

