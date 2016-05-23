# -*- coding:utf-8 -*-

from django.shortcuts import render
import logging
from .forms import *
from base.models import BillIn,BillInd,BasShop,Adpriced,Adprice,Ret0,Retitem0,BasProduct
from django.core.paginator import Paginator #分页查询
import time,datetime
from django.db import connection
from base.utils import MethodUtil as mtu

# Create your views here.
logger=logging.getLogger('base.supplier.stock.views')
# time = datetime.datetime.today().strftime("%Y-%m-%d")
# monthFrist = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
def supplierBill(request):
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    shopCodeList = []
    shopCode = ''
    code = ''
    start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    end = datetime.datetime.today().strftime("%Y-%m-%d")
    page = request.GET.get('page',1)

    if request.method== 'POST':
        form = BillInForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            shopCode = form.cleaned_data['shopcode']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
    else:
        code = request.GET.get('code','')
        shopCode = request.GET.get('shopcode','')
        start = request.GET.get('start',start)
        end = request.GET.get('end',end)
        data = {'code':code,'shopcode':shopCode,'start':start,'end':end}
        form = BillInForm(data)

    kwargs = {}
    if code:
        kwargs.setdefault("code__contains",code)
    if len(shopCode):
        shopCodeStr = shopCode[0:len(shopCode)-1]
        shopCodeList = shopCodeStr.split(',')
        kwargs.setdefault("shopcode__in",shopCodeList)
    kwargs.setdefault("chdate__gte",start)
    kwargs.setdefault("chdate__lte","{end} 23:59:59".format(end=end))
    kwargs.setdefault("orderstyle","2301")
    kwargs.setdefault("spercode",sperCode)
    kwargs.setdefault("grpcode",grpCode)

    billList = BillIn.objects.values("code","ordercode","chdate","spercode","spername","shopcode","inprice_tax","seenum","remark","sstyle")\
                                         .filter(**kwargs)

    totalInpriceTax = 0

    for item in billList:
        totalInpriceTax += item['inprice_tax']


    #分页函数
    paginator=Paginator(billList,20)
    try:
        billList=paginator.page(page)
    except Exception as e:
        print(e)

    return render(request,
                  'user_bill.html',
                  {"form":form,
                   "paginator":paginator,
                   "page":page,
                   "code":code,
                   "shopCode":shopCode,
                   "shopCodeList":shopCodeList,
                   "start":str(start),
                   "end":str(end),
                   "billList":billList,
                   "grpName":grpName,
                   "totalInpriceTax":totalInpriceTax
                   })


def billArticle(request):
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    code = request.GET.get('code',None)

    #供应商信息
    suppiler = BillIn.objects.values("spercode","spername","shopcode","seenum","chdate","edate").distinct().get(code=code)
    #更改查看次数
    seeNum = suppiler.get('seenum')
    if not seeNum:
        seeNum = 0
    setSeeNum(code,grpCode,seeNum+1)
    #门店信息
    shopCode = suppiler.get('shopcode')
    shopName = BasShop.objects.values('shopnm').get(shopcode=shopCode)

    #入库单明细
    billList = BillInd.objects.values("procode","pname","unit","taxrate","num","denums","prnum","price_intax","sum_tax","chdate","salebn","classes")\
                              .filter(code=code,orderstyle__in=('2323','2301'),grpcode=grpCode)\
                              .order_by('pname','classes','unit')

    TotalSumTax = 0  #含税进价总额
    sum1,sum2,sum3,sum4 = 0,0,0,0
    for bill in billList:
        TotalSumTax += bill.get('sum_tax',0)
        sum1 += bill["num"]
        sum2 += bill["denums"]
        sum3 += bill["prnum"]
        sum4 += bill["price_intax"]

    return render(request,'user_bill_article.html',locals())

def billAdjust(request):
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    billList = []
    shopCode = ''
    shopCodeList = []
    shopStr = ''
    code = ''
    start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    end = datetime.datetime.today().strftime("%Y-%m-%d")
    orderStyle = ''
    page = request.GET.get('page',1)

    if request.method== 'POST':
        form = AdPriceForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            shopCode = form.cleaned_data['shopcode']
            start = str(form.cleaned_data['start'])
            end = str(form.cleaned_data['end'])
            orderStyle = form.cleaned_data['orderStyle']
    else:
        code = request.GET.get('code','')
        shopCode = request.GET.get('shopcode','')
        start = request.GET.get('start',start)
        end = request.GET.get('end',end)
        orderStyle = request.GET.get('orderstyle','chdate')

        data = {'code':code,'shopcode':shopCode,'start':start,'end':end}
        form = AdPriceForm(data)

    if shopCode:
        shopStr=str(shopCode[0:len(shopCode)-1])
        shopCodeList = shopStr.split(",")
        shopCode ="'"
        for item in shopCodeList:
            shopCode +=str(item)
            shopCode +="','"
        shopCode = shopCode[0:len(shopCode)-2]
        sql = "select * from ( select adprice.adpriceclass,adprice.code,adprice.chdate,adprice.spercode,spername,shopcode,shopname,sum((adpriced.dqhsjj-adpriced.cprice_notax)*adpriced.anum) inprice_tax,seenum from adprice,adpriced where adprice.shopcode in ("+shopCode+") and adprice.code like '%"+code+"%' and adprice.chdate>='"+start+"' and adprice.chdate<='"+end+" 23:59:59' and adprice.spercode="+sperCode+" and adprice.grpcode="+grpCode+" group by adprice.adpriceclass,adprice.code,adprice.chdate,adprice.spercode,spername,shopcode,shopname,cstyle,csname,bdate,edate,remark,status,seenum ) as t1 order by "+orderStyle+" desc"
    else:
        sql = "select * from ( select adprice.adpriceclass,adprice.code,adprice.chdate,adprice.spercode,spername,shopcode,shopname,sum((adpriced.dqhsjj-adpriced.cprice_notax)*adpriced.anum) inprice_tax,seenum,cstyle,csname,bdate,edate,remark,status,sum(anum) anum from adprice,adpriced where adprice.code like '%"+code+"%' and adprice.chdate>='"+start+"' and adprice.chdate<='"+end+" 23:59:59' and adprice.code=adpriced.code and  adprice.spercode="+sperCode+" and adprice.grpcode="+grpCode+" group by adprice.adpriceclass,adprice.code,adprice.chdate,adprice.spercode,spername,shopcode,shopname,cstyle,csname,bdate,edate,remark,status,seenum ) as t1 order by "+orderStyle+" desc"

    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    cursor.close()
    connection.close()

    for obj in fetchall:
        dic={}
        dic['adpriceclass']=obj[0]
        dic['code']=obj[1]
        dic['chdate']=obj[2]
        dic['spercode']=obj[3]
        dic['spername']=obj[4]
        dic['shopcode']=obj[5]
        dic['shopname']=obj[6]
        dic['inprice_tax']=obj[7]
        dic['seenum']=obj[8]
        billList.append(dic)

    #分页函数
    paginator=Paginator(billList,20)
    try:
        billList=paginator.page(page)
    except Exception as e:
        print(e)

    return render(request,
                  'user_billAdjust.html',
                  {"form":form,
                   "paginator":paginator,
                   "page":page,
                   "code":code,
                   "shopCode":shopCode,
                   "shopCodeList":shopCodeList,
                   "shopStr":shopStr,
                   "start":str(start),
                   "end":str(end),
                   "billList":billList,
                   "orderStyle":orderStyle,
                   "grpName":grpName
                   })
def adjustArticle(request):
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    code = request.GET.get('code',None)

    # 供应商信息
    suppiler={}
    suppiler = Adprice.objects.values("spercode","spername","shopname","seenum","chdate","edate").distinct().get(code=code,spercode=sperCode)

    #更改查看次数
    seeNum = suppiler.get('seenum')
    if not seeNum:
        seeNum = 0
    Adprice.objects.filter(code=code,grpcode=grpCode).update(seenum=seeNum)

    #获取详情信息
    kwargs = {}
    if sperCode:
        kwargs.setdefault("spercode",sperCode)
    kwargs.setdefault("code",code)
    kwargs.setdefault("grpcode",grpCode)
    adBillList = Adpriced.objects.values("adbatchseq","pcode","pname","anum","cprice_notax","dqhsjj","spercode","barcode")\
                                 .filter(**kwargs)

    sum4=0  #含税调整金额
    sum5=0  #调整数量（合计）
    sum6=0  #含税调整金额（合计）
    for adObj in adBillList:
        sum4 = round((adObj.get('dqhsjj')-adObj.get('cprice_notax'))*adObj.get('anum'),3)
        adObj.setdefault("sum4",sum4)
        sum6+=sum4
        sum5+=round(adObj.get('anum'),3)

    return render(request,'user_billAdjust_article.html',locals())


def billBack(request):
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    shopCodeList = []
    shopCode = ''
    code = ''
    start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    end = datetime.datetime.today().strftime("%Y-%m-%d")
    page = request.GET.get('page',1)
    if request.method== 'POST':
        form = BillInForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            shopCode = form.cleaned_data['shopcode']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
    else:
        code = request.GET.get('code','')
        shopCode = request.GET.get('shopcode','')
        start = request.GET.get('start',start)
        end = request.GET.get('end',end)
        data = {'code':code,'shopcode':shopCode,'start':start,'end':end}
        form = BillInForm(data)
    kwargs = {}
    if grpCode:
        kwargs.setdefault("grpcode",grpCode)
    if code:
        kwargs.setdefault("code__contains",code)
    if len(shopCode):
        shopCodeStr = shopCode[0:len(shopCode)-1]
        shopCodeList = shopCodeStr.split(',')
        kwargs.setdefault("shopcode__in",shopCodeList)
    kwargs.setdefault("chdate__gte",start)
    kwargs.setdefault("chdate__lte","{end} 23:59:59".format(end=end))
    kwargs.setdefault("orderstyle","2323")
    kwargs.setdefault("spercode",sperCode)

    billList = BillIn.objects.values("code","ordercode","chdate","spercode","spername","shopcode","inprice_tax","seenum","remark","sstyle")\
                             .filter(**kwargs)
    totalInpriceTax = 0
    for item in billList:
        totalInpriceTax += item['inprice_tax']
    #分页函数
    paginator=Paginator(billList,20)
    try:
        billList=paginator.page(page)
    except Exception as e:
        print(e)

    return render(request,
                  'user_billBack.html',
                  {"form":form,
                   "paginator":paginator,
                   "page":page,
                   "code":code,
                   "shopCode":shopCode,
                   "shopCodeList":shopCodeList,
                   "start":str(start),
                   "end":str(end),
                   "billList":billList,
                   "grpName":grpName,
                   "totalInpriceTax":totalInpriceTax
                   })

def backArticle(request):
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    code = request.GET.get('code',None)

    #供应商信息
    suppiler = BillIn.objects.values("spercode","spername","shopcode","seenum","chdate","edate").distinct().get(code=code)
    #更改查看次数
    seeNum = suppiler.get('seenum')
    if not seeNum:
        seeNum = 0
    setSeeNum(code,grpCode,seeNum+1)
    #门店信息
    shopCode = suppiler.get('shopcode')
    shopName = BasShop.objects.values('shopnm').get(shopcode=shopCode)

    billList = BillInd.objects.values("procode","pname","unit","taxrate","num","denums","prnum","price_intax","sum_tax","chdate","salebn","classes")\
                              .filter(code=code,orderstyle__in=('2323','2301'),grpcode=grpCode)\
                              .order_by('pname','unit')#order_by('pname','class'，'unit')

    TotalSumTax = 0  #含税进价总额
    sum1,sum2 = 0,0
    for bill in billList:
        TotalSumTax += bill.get('sum_tax',0)
        sum1 += bill["denums"]
        sum2 += bill["price_intax"]

    return render(request,'user_billback_article.html',locals())


def setSeeNum(code,grpcode,seeNum):
    BillIn.objects.filter(code=code,grpcode=grpcode).update(seenum=seeNum)

def beforeBackBill(request):
    """
    预退货单列表
    :param request:
    :return:
    """
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    shopCodeList = []

    start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    end = datetime.datetime.today().strftime("%Y-%m-%d")
    page = mtu.getReqVal(request,'page',1)

    sheetId =  mtu.getReqVal(request,'sheetId','')
    shopCode =  mtu.getReqVal(request,'shopCode','')
    start =  mtu.getReqVal(request,'start',start)
    end =  mtu.getReqVal(request,'end',end)

    kwargs = {}
    if sheetId:
        kwargs.setdefault("sheetid__contains",sheetId)
    if len(shopCode):
        shopCodeStr = shopCode[0:len(shopCode)-1]
        shopCodeList = shopCodeStr.split(',')
        kwargs.setdefault("shopid__in",shopCodeList)

    kwargs.setdefault("checkdate__gte",start)
    kwargs.setdefault("checkdate__lte","{end} 23:59:59".format(end=end))

    kwargs.setdefault("venderid",sperCode)
    kwargs.setdefault("flag",2)

    billList = Ret0.objects.values("sheetid","shopid","venderid","retdate","editdate","paymoney","kxsummoney","acceptflag","badflag","checkdate","notes")\
                             .filter(**kwargs).order_by("sheetid")
    #分页函数
    paginator=Paginator(billList,20)
    try:
        billList=paginator.page(page)
    except Exception as e:
        print(e)

    ACCEPT_FLAG = {"0":"同意","1":"不同意"}
    BAD_FLAG = {"0":"坏货","1":"好货"}

    return render(request,'user_bill_beforeback.html',locals())

def beforeBackDetail(request):
    """
    预退货单明细
    :param request:
    :return:
    """
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')
    sheetid = request.GET.get('sheetId',None)

     #供应商信息
    bill = Ret0.objects.values("shopid","checkdate","editdate").distinct().get(sheetid=sheetid)

    #门店信息
    shopCode = bill.get('shopid')
    shop = BasShop.objects.values('shopnm').get(shopcode=shopCode)

    billList = Retitem0.objects.values("sheetid","goodsid","deptid","taxrate","price","cost",
                                       "askqty","planqty","realqty","reasontypeid","reason",
                                       "logistics","pknum","pkname","pkspec","subitem_iid",
                                       "stockqty","goodscostid","notes","inputgoodsid"
                                       ).filter(sheetid=sheetid).order_by('goodsid','deptid')

    sum1,sum2,sum3,sum4,sum5,sum6 = 0,0,0,0,0,0
    for item in billList:
        plist = BasProduct.objects.values("pcode","chnm","barcode").filter(pcode=str(item["goodsid"]));
        goodsname = ""
        barcode = ""
        if plist:
            goods = plist[0]
            goodsname = goods["chnm"]
            barcode = goods["barcode"]
        item["goodsname"] = goodsname
        item["barcode"] = barcode
        sum1 += item["price"]
        sum2 += item["cost"]
        sum3 += item["planqty"]
        sum4 += item["realqty"]
        sum5 += item["stockqty"]
        sum6 += item["pknum"]

    return render(request,'user_billbeforeback_article.html',locals())