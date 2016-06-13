#-*- coding:utf-8 -*-
__author__ = 'liubf'

import json,datetime
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q,Sum
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from base.models import OrdStatus,Ord,OrdD,BasShop,BasSupplier
from base.utils import MethodUtil
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

    inflag =  MethodUtil.getReqVal(request,"inflag","")    #验收状态

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

    if inflag and inflag!="":
        karrs.setdefault("inflag",inflag)

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

    for item in pubList:
        slist = OrdStatus.objects.filter(ordercode=item["ordercode"]).values("status")
        if slist:
            item["status"] = slist[0]["status"]

    page = Paginator(pubList,__EACH_PAGE_SHOW_NUMBER,allow_empty_first_page=True).page(int(pageNum))

    result = {"page":page,"pageNum":str(pageNum)}
    result.setdefault("shopCode",shopcode)
    result.setdefault("status",status)
    result.setdefault("grpname",grpname)
    result.setdefault("state",state)
    result.setdefault("inflag",inflag)
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
    slist = OrdStatus.objects.filter(ordercode=ordercode).values("ordercode","yyshdate","status")

    orderstatus = {}
    if not slist:
        orderstatus["yyshdate"] = order.sdate
    else:
        sobj = slist[0]
        if not sobj["yyshdate"]:
            orderstatus["yyshdate"] = order.sdate
        else:
            orderstatus = slist[0]

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

    sum1,sum2,sum3 = 0,0,0
    for item in detailList:
        sum1 += item["denums"]
        sum2 += item["price_intax"]
        sum3 += item["denums"] * item["price_intax"]
        item["jshj"] = item["denums"] * item["price_intax"]
    today = datetime.datetime.today()

    #查询门店信息
    shop = BasShop.objects.get(grpcode=grpcode,shopcode=order.shopcode)
    if shop.tel:
        shop.tel = shop.tel.strip()
    else:
        shop.tel = ""

    if shop.shopnm:
        shop.shopnm = shop.shopnm.strip()

    #查询供应商信息
    slist = BasSupplier.objects.filter(suppcode=order.spercode).values("suppcode","chnm","linkmen","phone1","phone2","paytypeid")
    if slist:
        supp = slist[0]
        if not supp["phone1"]:
            if supp["phone2"]:
                supp["phone1"] = supp["phone2"].strip()
        else:
           supp["phone1"] = supp["phone1"].strip()
    else:
        supp = {}

    return render(request,"user_order_article.html",locals())

#保存预约送货日期
@csrf_exempt
@transaction.non_atomic_requests
def save(request):
    ordercode = MethodUtil.getReqVal(request,"ordercode","")
    yyshdate = MethodUtil.getReqVal(request,"yyshdate","")
    grpcode = request.session.get("s_grpcode")

    response_data = {}
    try:
        if ordercode:
            #1.更新订单明细
            # detailList = OrdD.objects \
            #                  .filter(ordercode=ordercode,grpcode=grpcode) \
            #                  .values("ordercode","procode","barcode","grpcode")

            # for row in detailList:  procode=str(row["procode"])
            OrdD.objects.filter(ordercode=ordercode,grpcode=grpcode).update(sjshsum="-1",sjprnum="-1")

            #2.保存预约送货日期 更新订单状态
            rs = OrdStatus.objects.all().filter(ordercode=ordercode)
            if not rs:
                OrdStatus.objects.create(ordercode=ordercode, yyshdate=yyshdate, status="Y")
            else:
                OrdStatus.objects.filter(ordercode=ordercode).update(yyshdate=yyshdate,status="Y")

            response_data['result'] = 'success'
        else:
             response_data['result'] = 'failure'
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
