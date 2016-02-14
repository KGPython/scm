# -*- coding:utf-8 -*-
from django.shortcuts import render
import logging
from .forms import *
from django.db.models import Q
from base.models import Billhead0,Billheaditem0,BasSupplier
from django.core.paginator import Paginator  #分页查询
import time,datetime

# Create your views here.
logger=logging.getLogger('base.supplier.stock.views')
time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
monthFrist = (datetime.datetime.now() - datetime.timedelta(days = 60)).strftime("%Y-%m-%d")
def balance(request):
    grpCode = request.session.get('s_grpcode','')
    grpName = request.session.get('s_grpname','')

    start = monthFrist
    end = time
    shopId = []
    sheetId = ''
    venderId = ''
    status = ''
    orderStyle = '-editdate'

    page = request.GET.get('page',1)
    if request.method== 'POST':
        form = BillInForm(request.POST)
        if form.is_valid():
            shopId = form.cleaned_data['shopid']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            sheetId = form.cleaned_data['sheetId']
            venderId = form.cleaned_data['venderId']
            status = form.cleaned_data['status']
            orderStyle = form.cleaned_data['orderStyle']
    else:

        shopId = request.GET.get('shopid','')
        start = request.GET.get('start',monthFrist)
        end = request.GET.get('end',time)
        sheetId = request.GET.get('sheetid','')
        venderId = request.GET.get('venderId','')
        status = request.GET.get('status','')
        orderStyle = request.GET.get('orderstyle','-enddate')
        form = BillInForm({"start":start,"end":end,"sheetid":sheetId,"venderId":venderId,"shopid":shopId,"status":status,"orderStyle":orderStyle})
    
    kwargs = {}
    if status:
        if status=="Y":
            kwargs.setdefault('status__contains',status)
    if sheetId:
        kwargs.setdefault('sheetid__contains',sheetId.strip())
    if venderId:
        kwargs.setdefault('venderid__contains',venderId.strip())
    if len(shopId):
        shopId = shopId[0:(len(shopId)-1)]
        shopId =shopId.split(',')
        kwargs.setdefault('shopid__in',shopId)
    kwargs.setdefault('begindate__gte',start)
    kwargs.setdefault('enddate__lte',"{end} 23:59:59".format(end=end))
    kwargs.setdefault('grpcode',grpCode)

    balanceList = Billhead0.objects.values("shopid","venderid","vendername","sheetid","begindate","enddate","editdate","flag","status","seenum","contracttype")\
                                   .filter(**kwargs).order_by(orderStyle)
    for row in balanceList:
        venderid = row["venderid"]
        supp = BasSupplier.objects.filter(suppcode=venderid).values("chnm")
        if supp:
            row["vendername"] = supp[0]["chnm"]

    paginator=Paginator(balanceList,20)
    try:
        balanceList=paginator.page(page)
    except Exception as e:
        print(e)

    # shopCodedistinct = []  #查询结果中，去重复的门店列表
    # for balance in balanceList:
    #     if balance.get('shopid') not in shopCodedistinct:
    #         shopCodedistinct.append(balance.get('shopid'))

    shopCodeStr = ''    #返回给pageFrom内部的shopcode表单
    for shop in shopId:
        shopCodeStr += shop+','

    return render(request,
                  'admin/retail_settle.html',
                  {"form":form,
                   "shopId":shopId,
                   "start":str(start),
                   "end":str(end),
                   "sheetId":sheetId,
                   "venderId":venderId,
                   "shopCodeStr":shopCodeStr,
                   # "shopCodedistinct":shopCodedistinct,
                   "status":status,
                   "orderStyle":orderStyle,
                   "balanceList":balanceList,
                   "page":page,
                   "grpName":grpName
                   })



def balanceArticle(request):
    grpCode = request.session.get('Curgrpcode','')
    grpName = request.session.get('s_grpname','')
    sheetId = request.GET.get('sheetid','')

    #结算通知单汇总
    balanceList = Billhead0.objects.values("shopid","venderid","vendername","sheetid","paytype","begindate","enddate"
                                               ,"editdate","curdxvalue","payablemoney","kxinvoice","kxmoney","kxcash",
                                               "premoney","editor","checker","paychecker","contracttype")\
                                       .get(sheetid__contains=sheetId)


    if balanceList.get('kxinvoice'):
        cfpkx = float(round(balanceList.get('kxinvoice'),2))
    else:
        cfpkx = 0

    zkkx = float(round(balanceList.get('kxmoney')-balanceList.get('kxcash'),2))#帐扣扣项

    if balanceList.get('curdxvalue'):
        curdxValue = balanceList.get('curdxvalue')
    else:
        curdxValue = 0

    if balanceList.get('payablemoney'):
        payableMoney = float(balanceList.get('payablemoney'))
    else:
        payableMoney= 0

    if balanceList.get('premoney'):
        premoney = float(balanceList.get('premoney'))
    else:
        premoney = 0

    if curdxValue == 0:
        invoicePay = round((payableMoney-cfpkx),2)#应开票金额
        realPay = round((payableMoney-zkkx-premoney),2)#实付金额
    else:
        invoicePay = round((curdxValue-cfpkx),2)
        realPay = round((curdxValue-zkkx-premoney),2)


    #结算通知明细
    balanceItems = Billheaditem0.objects.values("inshopid","refsheettype","refsheetid","managedeptid","payabledate",
                                                "costvalue","costtaxvalue","costtaxrate")\
                                        .filter(sheetid__contains=sheetId)\
                                        .order_by("refsheettype","refsheetid","inshopid")

    totalCostValue = 0
    totalCostTax = 0
    i = 0
    for item in balanceItems:
        totalCostValue += item.get('costvalue',0)   #应结金额总额
        totalCostTax += item.get('costtaxvalue',0)  #税金总额
        i+=1
        item['lineIndex'] = i   #每条记录的行号
        item['managedeptid'] = str(item.get('managedeptid',0))

    payTypeDict = {"0":"其他","1":"支票","2":"电汇","3":"汇票"}

    return render(request,'admin/retail_settle_article.html',locals())