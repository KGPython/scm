"""scm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from base.supplier.bill.views import *

urlpatterns = [
    url(r'^bill/billin/$', supplierBill , name='supplierBill'),
    url(r'^bill/inArticle/', billArticle, name='billArticle'),
    url(r'^bill/billAdjust/$', billAdjust , name='billAdjust'),
    url(r'^bill/adjustArticle/', adjustArticle , name='adjustArticle'),
    url(r'^bill/billBack/$', billBack , name='billBack'),
    url(r'^bill/backArticle/$', backArticle , name='backArticle'),

    url(r'^bill/billBeforeBack/$', beforeBackBill, name='billBeforeBack'),
    url(r'^bill/beforeBackArticle/$', beforeBackDetail , name='beforeBackArticle'),
]
