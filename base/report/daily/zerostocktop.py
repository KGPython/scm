#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
     print('zero stock')
     tlist = []
     for i in range(1,300):
         item = ['C0%s' % i,'Test%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i,'%s'%i]
         tlist.append(item)
     return render(request,"report/daily/zero_stock_top.html",{'tlist':tlist})

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass