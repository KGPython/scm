#-*- coding:utf-8 -*-
__author__ = 'liubf'

import os,xlrd,xlwt3 as xlwt
import time,datetime
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from base.models import BasUser,BasGoods
from base.utils import Constants,MethodUtil as mtu
from base.views import findShop

__EACH_PAGE_SHOW_NUMBER = 10

#供应商商品基本信息
def index(request):
    grpname = request.session.get("s_grpname","")
    result = {"grpname":grpname,"shopnames":"","pageNum":"1","flag":"0"}

    return render(request,"user_base.html",result)

#根据条件查询供应商商品信息
@csrf_exempt
def query(request):
    #接收前台参数，不区别get/post方法
    grpname = request.session.get("s_grpname","")
    grpcode = request.session.get("s_grpcode")
    suppcode = request.session.get("s_suppcode")

    qtype = mtu.getReqVal(request,"qtype","1")
    pageNum = mtu.getReqVal(request,"pageNum","1")
    shopcode =  mtu.getReqVal(request,"shopCode","")
    barcode =  mtu.getReqVal(request,"barcode","")
    goodsName =  mtu.getReqVal(request,"goodsName","")
    orderstyle =  mtu.getReqVal(request,"orderstyle","")
    flag = mtu.getReqVal(request,"flag","")

    #组合查询条件
    q = Q()
    karrs = {}
    shopnames = ""
    shopList = findShop()

    #设置默认查询条件
    q.add(~Q(grpcode=""),Q.AND)
    karrs.setdefault("grpcode",grpcode)
    karrs.setdefault("venderid",suppcode)
    if shopcode:
        clist = []
        codes = shopcode.split(",")
        for i in range(0,len(codes)):
            if codes[i]:
                clist.append(codes[i])
                shopnames+="%s," % shopList[str(codes[i])]
        karrs.setdefault('shopid__in',clist)

    if barcode:
        karrs.setdefault('barcodeid__icontains',barcode.strip())
    if goodsName:
        karrs.setdefault("name__icontains",goodsName.strip())
    #商品状态
    if flag:
        q.add(Q(flag=flag),Q.AND)

    #设置默认排序方式
    orderby = orderstyle
    if not orderby:
        orderby = "shopid"

    #分页查询数据
    pubList = BasGoods.objects \
        .filter(q,**karrs) \
        .order_by("-"+orderby) \
        .values("grpcode","name","unitname","spec","brandid","deptid","deptname","goodsid","shopid","venderid","cost",
                "costtaxrate","dkrate","promflag","startdate","enddate","flag","price","barcodeid")

    page = Paginator(pubList,__EACH_PAGE_SHOW_NUMBER,allow_empty_first_page=True).page(int(pageNum))

    if qtype=='1':
        result = {"page":page,"pageNum":str(pageNum),"gstatus":Constants.SALE_STATUS}
        result.setdefault("promflag",Constants.PROM_FLAG)
        result.setdefault("shopCode",shopcode)
        result.setdefault("barcode",barcode)
        result.setdefault("goodsName",goodsName)
        result.setdefault("orderstyle",orderstyle)
        result.setdefault("flag",flag)
        result.setdefault("grpname",grpname)
        result.setdefault("shopnames",shopnames[0:len(shopnames)-1])
        return render(request,"user_base.html",result)
    else:
        return exportXls(pubList)

#导出商品信息
def exportXls(rslist):

    sname = "商品资料一览表"

    titles = [("门店编码","1000","shopid"),("门店名称","1000","shopid"),("商品条码","1000","barcodeid"),("商品名称","5000","name"),("规格","500","spec"),
              ("进价","500","cost"),("执行售价","1000","price"),("销售状态","1000","flag"),("供应商","1000","venderid"),("税率","500","costtaxrate"),
              ("单位","500","unitname"),("小类","1000","deptid"),("商品编码","1000","goodsid"),("促销标志","1000","promflag"),("开始日期","1000","startdate"),
              ("结束日期","1000","enddate")]

    fmtlist = [None,None,None,None,None,None,None,None,None,None,
               None,None,None,None,"%Y-%m-%d","%Y-%m-%d"]

    shopDict = findShop()

    dictlist = [None,shopDict,None,None,None,None,None,Constants.SALE_STATUS,None,
               None,None,None,None,Constants.PROM_FLAG,None,None]

    book = mtu.exportXls(sname,titles,rslist,None,dictlist,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "goods.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response