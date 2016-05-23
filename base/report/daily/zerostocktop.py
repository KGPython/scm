#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.models import RepShopZeroStock

@csrf_exempt
def index(request):
     print('zero stock')
     tlist = []
     for i in range(1,22):
         item = ['C0%s' % i,'Test%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i]
         tlist.append(item)

     tlist2 = []
     for i in range(1,22):
         item = ['1%s' % i,'课组%s'%i,'%s'%i,'%s'%i,'%s'%i]
         tlist2.append(item)

     rlist = RepShopZeroStock.objects.all().order_by("shopid");
     for item in rlist:
         print(item.shopid)
         #1.计算门店总排名

     return render(request,"report/daily/zero_stock_top.html",{'tlist':tlist,'tlist2':tlist2})

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass