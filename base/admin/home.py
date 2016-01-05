# -*- coding:utf-8 -*-
__author__ = 'End-e'
from django.shortcuts import render
from django.core.paginator import Paginator

from base.message.views import findPubInfoAllByCon

__EACH_PAGE_SHOW_NUMBER = 10

def index(request):
    user = request.session.get("s_user",None)
    if user:
         pubList = findPubInfoAllByCon(user)
    else:
         pubList = []

    pageNum = int(request.GET.get("pageNum",1))

    page =  Paginator(pubList,__EACH_PAGE_SHOW_NUMBER,allow_empty_first_page=True).page(pageNum)

    return render(request,"admin/index.html",{"page":page,"pageNum":pageNum})

def repwd(request):

    return render(request, 'admin/sysConf_retail_setpwd.html')
