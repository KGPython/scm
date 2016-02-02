#-*- coding:utf-8 -*-
__author__ = 'liubf'

import os,xlrd,json,xlwt3 as xlwt
import time,datetime
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q,Sum
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from base.models import BasUser,Ord,OrdD,BasShop
from base.utils import Constants,MethodUtil
from base.views import findShop

__EACH_PAGE_SHOW_NUMBER = 10

#供应商商品基本信息
def index(request):
    grpname = request.session.get("s_grpname")

    start = (datetime.datetime.now() - datetime.timedelta(days = 7)).strftime("%Y-%m-%d")
    end = datetime.datetime.today().strftime("%Y-%m-%d")
    sum = 0.0

    result = {"grpname":grpname,"shopnames":"","start":start,"end":end,"pageNum":"1","sum":sum}

    return render(request,"user_order.html",result)

#根据条件查询供应商商品信息
@csrf_exempt
def query(request):
    user = request.session.get("s_user")
    suppcode = request.session.get("s_suppcode")
    utype = request.session.get("s_utype")
    grpname = request.session.get("s_grpname")
    dept = user["dept"]

    pageNum = MethodUtil.getReqVal(request,"pageNum","1")    #页码
    shopcode =  MethodUtil.getReqVal(request,"shopCode","")  #门店编号
    status =  MethodUtil.getReqVal(request,"status","A")   #确认状态
    state =  MethodUtil.getReqVal(request,"state","")    #过期状态
    logistics = MethodUtil.getReqVal(request,"logistics","")  #订单类型
    start = MethodUtil.getReqVal(request,"start","")   #审核日期：开始时间
    end = MethodUtil.getReqVal(request,"end","")  #审核日期：结束时间
    orderstyle =  MethodUtil.getReqVal(request,"orderstyle","")   #排序条件
    ordercode = MethodUtil.getReqVal(request,"ordercode","")   #订单编号

    #组合查询条件
    shopnames = ""
    karrs = {}
    karrs.setdefault("spercode",suppcode)   #供应商ID
    shopList = findShop()

    if utype=="1":
         karrs.setdefault('shopid',dept)
    else:
        if shopcode:
            clist = []
            codes = shopcode.split(",")
            for i in range(0,len(codes)):
                if codes[i]:
                    clist.append(codes[i])
                    shopnames+="%s," % shopList[str(codes[i])]
            karrs.setdefault('shopcode__in',clist)

    if ordercode:
        karrs.setdefault('ordercode__icontains',ordercode.strip())

    if status and status!="A":
        karrs.setdefault("status",status)

    if state=='Y':
        karrs.setdefault("sdate__lt",datetime.datetime.now().strftime("%Y-%m-%d"))
    elif state=='N':
        karrs.setdefault("sdate__gte",datetime.datetime.now().strftime("%Y-%m-%d"))

    if logistics and logistics!="A":
        karrs.setdefault("logistics",logistics)

    if start:
        karrs.setdefault("checkdate__gte",(start))
    else:
        karrs.setdefault("checkdate__gte",(datetime.datetime.now() - datetime.timedelta(days = 7)).strftime("%Y-%m-%d"))

    if end:
        karrs.setdefault("checkdate__lte","{end} 23:59:59".format(end=end))
    else:
        karrs.setdefault("checkdate__lte","{end} 23:59:59".format(end=datetime.datetime.now().strftime("%Y-%m-%d")))

    #设置默认排序方式
    orderby = orderstyle
    if not orderby:
        orderby = "sdate"

    #含税进价金额合计
    sumList = Ord.objects.filter(**karrs).aggregate(taxSum = Sum("inprice_tax"))
    if not sumList["taxSum"]:
        sumList["taxSum"] = 0.0

    #分页查询数据
    pubList = Ord.objects \
        .filter(**karrs) \
        .order_by("inflag","-"+orderby) \
        .values("remark","logistics","inflag","ordercode","checkdate","concode","style","spercode","spername","status","sdate",
                "shopcode","inprice_tax","printnum","seenum","purday","spsum","sjshsum","ssspzb")

    page = Paginator(pubList,__EACH_PAGE_SHOW_NUMBER,allow_empty_first_page=True).page(int(pageNum))

    result = {"page":page,"pageNum":str(pageNum)}
    result.setdefault("shopCode",shopcode)
    result.setdefault("status",status)
    result.setdefault("grpname",grpname)
    result.setdefault("state",state)
    result.setdefault("logistics",logistics)
    result.setdefault("start",start)
    result.setdefault("end",end)
    result.setdefault("ordercode",ordercode)
    result.setdefault("orderstyle",orderstyle)
    result.setdefault("today",datetime.datetime.today())
    result.setdefault("shopnames",shopnames[0:len(shopnames)-1])
    result.setdefault("sum",'%.4f' % sumList["taxSum"])
    return render(request,"user_order.html",result)

#查询订单详情
@csrf_exempt
def find(request):

    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname")

    ordercode = MethodUtil.getReqVal(request,"ordercode","")

    #查询订单信息
    order = Ord.objects.get(ordercode=ordercode)

    if not order.yyshdate:
        order.yyshdate = order.sdate

    seenum = order.seenum
    if not seenum:
        seenum = 0

    #更新订单查询次数
    Ord.objects.filter(ordercode=ordercode).update(seenum=int(seenum)+1)

    #查询订单明细
    detailList = OrdD.objects \
        .filter(ordercode=ordercode,grpcode=grpcode) \
        .order_by("rowno","procode","unit","num") \
        .values( "drrq","ordercode","rid","procode","salebn","pn","classes","unit","taxrate","num","innums","denums","price_intax","sum_intax","nums_inplan",
                    "date_inplan","checkdate","prnum","barcode","rowno","grpcode","sjshsum","ssnumzb","sjprnum","promflag","refsheetid")

    today = datetime.datetime.today()

    #查询门店信息
    shop = BasShop.objects.get(grpcode=grpcode,shopcode=order.shopcode)

    return render(request,"user_order_article.html",{"order":order,"detailList":detailList,"today":today,"shop":shop,"curgrpname":grpname})

#保存预约送货日期
@csrf_exempt
@transaction.non_atomic_requests
def save(request):
    ordercode = MethodUtil.getReqVal(request,"ordercode","")
    yyshdate = MethodUtil.getReqVal(request,"yyshdate","")
    grpcode = request.session.get("s_grpcode")

    response_data = {}
    try:


        #1.更新订单明细
        detailList = OrdD.objects \
                         .filter(ordercode=ordercode,grpcode=grpcode) \
                         .values("ordercode","procode","barcode","grpcode")

        for row in detailList:
            OrdD.objects.filter(ordercode=ordercode,grpcode=grpcode,procode=str(row["procode"])).update(sjshsum="-1",sjprnum="-1")    #note="

        #2.保存预约送货日期，更新订单状态
        Ord.objects.filter(ordercode=ordercode).update(yyshdate=yyshdate,status="Y")

        response_data['result'] = 'success'
    except Exception as e:
        print(e)
        response_data['result'] = 'failure'
        transaction.rollback()
    else:
        transaction.commit()

    return HttpResponse(json.dumps(response_data), content_type="application/json")

#更新打印次数
@csrf_exempt
def upprint(request):
    ordercode = request.POST.get("ordercode","")

    #查询订单明细
    order = Ord.objects.get(ordercode=ordercode)
    printnum = order.printnum
    if not printnum:
        printnum = 0
    else:
        printnum = int(printnum)

    printnum += 1
    Ord.objects.filter(ordercode=ordercode).update(printnum=printnum)

    return  HttpResponse(json.dumps({"printnum":printnum}), content_type="application/json")
