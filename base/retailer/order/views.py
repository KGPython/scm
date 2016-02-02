# -*- coding:utf-8 -*-
from django.shortcuts import render
from .form import *
from base.models import Ord,BasUserClass,OrdD
import time,datetime
from django.core.paginator import Paginator
from django.db.models import Q

nowTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
def retOrder(request):
    grpCode = request.session.get('s_grpcode','')
    grpName = request.session.get('s_grpname','')
    userRoleList = request.session.get('s_rcodes',[])

    status=''
    state=''
    sperCode =''
    orderCode=''
    start=''
    end=''
    shopCode=''
    orderStyle=''

    if request.method == 'POST':
        form = retOrderForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            state  = form.cleaned_data['state']
            sperCode  = form.cleaned_data['spercode']
            orderCode  = form.cleaned_data['ordercode']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            shopCode = form.cleaned_data['shopcode']
            orderStyle = form.cleaned_data['orderstyle']
        else:
            print(form.errors)
    else:
        status = request.GET.get('status','')
        state  = request.GET.get('state','')
        sperCode  = request.GET.get('spercode','')
        orderCode  = request.GET.get('ordercode','')
        start = request.GET.get('start',(datetime.datetime.now() - datetime.timedelta(days = 2)).strftime("%Y-%m-%d"))
        end = request.GET.get('end',nowTime)
        shopCode = request.GET.get('shopcode','')
        orderStyle = request.GET.get('orderstyle','checkdate')
        data = {'status':status,"state":state,"spercode":sperCode,"ordercode":orderCode,"start":start,"end":end,"shopcode":shopCode,'orderstyle':orderStyle}
        form = retOrderForm(data)

    kwargs = {}
    if status:
        kwargs.setdefault('status',status)

    if state == 'Y':
        kwargs.setdefault('sdate__lt',nowTime)
    else:
        kwargs.setdefault('sdate__gte',nowTime)

    if sperCode:
        kwargs.setdefault('spercode',sperCode)
    if orderCode:
        kwargs.setdefault('ordercode__contains',orderCode)
    if len(shopCode):
        shopStr= shopCode[0:(len(shopCode)-1)]
        shopList =shopStr.split(',')
        kwargs.setdefault('shopcode__in',shopList)

    kwargs.setdefault('checkdate__gte',start)
    kwargs.setdefault('checkdate__lte',end)
    kwargs.setdefault('grpcode',grpCode)
    retOrderList = {}
    print(userRoleList)
    if '1' in userRoleList:
        retOrderList = Ord.objects.values('ordercode','checkdate','state','status','style','spercode','spername','sdate','shopcode','inprice_tax','seenum','printnum')\
                                        .filter(**kwargs).order_by("-"+orderStyle)
    else:
        shopRole = BasUserClass.objects.values('orgcode').filter(ucode__in=userRoleList,tablecode='roleshop')

        q=Q()
        q.add(Q(shopcode__in=shopRole),Q.AND)

        retOrderList = Ord.objects.values('ordercode','checkdate','state','status','style','spercode','spername','sdate','shopcode','inprice_tax','seenum','printnum')\
                                  .filter(q,**kwargs).order_by("-"+orderStyle)

    totalInpriceTax = 0
    for item in retOrderList:
        totalInpriceTax += float(item['inprice_tax'])
        # print(totalInpriceTax)
    page = request.GET.get('page',1)
    paginator = Paginator(retOrderList,10)
    try:
        retOrderList = paginator.page(page)
    except Exception as e:
        print(e)

    return render(request,
                  'admin/retail_order.html',
                  {
                    "status":status,
                    "state":state,
                    "sperCode":sperCode,
                    "orderCode":orderCode,
                    "start":str(start),
                    "end":str(end),
                    "shopCode":shopCode,
                    "orderStyle":orderStyle,
                    "retOrderList":retOrderList,
                    "today":datetime.datetime.today(),
                    "page":page,
                    "form":form,
                    "totalInpriceTax":totalInpriceTax,
                    "grpName":grpName
                  })


def retOrderArticle(request):
    grpCode = request.session.get('s_grpcode','')
    grpName = request.session.get('s_grpname','')
    orderCode = request.GET.get('ordercode','')

    #订单中供应商信息
    sperDict = Ord.objects.values('shopcode','sdate','spercode','spername','purdate','remark','yyshdate').get(ordercode=orderCode)
    #订单明细列表
    retOrderList = OrdD.objects.values('procode','pn','unit','taxrate','innums','denums','price_intax','sum_intax','sjshsum','sjprnum')\
                               .filter(ordercode=orderCode)

    sumDenums = 0
    sumSumIntax = 0
    for item in retOrderList:
        sumDenums += item['denums']
        sumSumIntax += item['sum_intax']

    return render(request,'admin/retail_order_article.html',locals())