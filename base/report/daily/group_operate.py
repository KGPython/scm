#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import Kshopsale,BasShopRegion,Estimate
import datetime,calendar,decimal

@csrf_exempt
def index(request):
     karrs = {}

     date = DateUtil.get_day_of_day(-1)
     days = date.day
     year = date.year
     month = date.month

     start = (date.replace(day=1)).strftime("%Y-%m-%d")
     yesterday = date.strftime("%Y-%m-%d")
     lastDay = calendar.monthrange(year,month)[1]

     #查询所有超市门店
     slist = BasShopRegion.objects.values("shopid","shopname","region","opentime","type").order_by("region","shopid")

     #查询当月销售
     karrs.setdefault("sdate__gte","{start} 00:00:00".format(start=start))
     karrs.setdefault("sdate__lte","{end} 23:59:59".format(end=yesterday))
     baselist = Kshopsale.objects.values('shopid','sdate','salevalue','salegain','tradenumber','tradeprice','salevalueesti','salegainesti',
                                         'sdateold','tradenumberold','tradepriceold','salevalueold','salegainold').filter(**karrs).order_by("shopid")

     karrs.clear()
     karrs.setdefault("sdate__year","{year}".format(year=year))
     yearlist = Kshopsale.objects.values("shopid")\
                     .filter(**karrs).order_by("shopid")\
                     .annotate(salevalue=Sum('salevalue')/10000,salegain=Sum('salegain')/10000,tradenumber=Sum('tradenumber')
                                              ,tradeprice=Sum('tradeprice'),salevalueesti=Sum('salevalueesti')/10000
                                              ,salegainesti=Sum('salegainesti')/10000,sdateold=Sum('sdateold')
                                              ,tradenumberold=Sum('tradenumberold'),tradepriceold=Sum('tradepriceold')
                                              ,salevalueold=Sum('salevalueold')/10000,salegainold=Sum('salegainold')/10000)

     ddict,mdict,edict,yeardict = {},{},{},{}
     itemShopId = None
     for item in baselist:
         sdate = item["sdate"].strftime("%Y-%m-%d")
         shopid = item["shopid"]
         #当日销售
         if sdate == yesterday:
            ddict.setdefault(str(item["shopid"]),item)

         if itemShopId != shopid:
            #月累计
            monthItem = {}
            monthItem.setdefault("shopid",shopid)
            monthItem.setdefault("m_salevalue",decimal.Decimal("0.00"))
            monthItem.setdefault("m_salevalueesti",decimal.Decimal("0.00"))
            monthItem.setdefault("m_salevalueold",decimal.Decimal("0.00"))
            monthItem.setdefault("m_salegain",decimal.Decimal("0.00"))
            monthItem.setdefault("m_salegainesti",decimal.Decimal("0.00"))
            monthItem.setdefault("m_salegainold",decimal.Decimal("0.00"))
            monthItem.setdefault("m_tradenumber",0)
            monthItem.setdefault("m_tradenumberold",0)
            monthItem.setdefault("m_tradeprice",decimal.Decimal("0.00"))
            monthItem.setdefault("m_tradepriceold",decimal.Decimal("0.00"))
            mdict.setdefault(shopid,monthItem)

            #日销售、毛利
            eitem = {}
            eitem.setdefault("shopid",shopid)
            eitem.setdefault("m_salevalue",decimal.Decimal("0.00"))
            eitem.setdefault("m_salevalueesti",decimal.Decimal("0.00"))
            eitem.setdefault("m_salegain",decimal.Decimal("0.00"))
            eitem.setdefault("m_salegainesti",decimal.Decimal("0.00"))

            for d in range(1,lastDay+1):
                salevalue = "salevalue_{year}{month}{day}".format(year=year,month=month,day=d)
                salevalueesti = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=d)
                saledifference = "saledifference_{year}{month}{day}".format(year=year,month=month,day=d)
                accomratio = "saleaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
                eitem.setdefault(salevalue,0.0)
                eitem.setdefault(salevalueesti,0.0)
                eitem.setdefault(saledifference,0.0)
                eitem.setdefault(accomratio,"0.0%")

                salegain = "salegain_{year}{month}{day}".format(year=year,month=month,day=d)
                salegainesti = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=d)
                salegaindifference = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=d)
                salegainaccomratio = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
                eitem.setdefault(salegain,0.0)
                eitem.setdefault(salegainesti,0.0)
                eitem.setdefault(salegaindifference,0.0)
                eitem.setdefault(salegainaccomratio,"0.0%")

            edict.setdefault(shopid,eitem)

         #月累计
         monthItem["m_salevalue"] += item["salevalue"]
         monthItem["m_salevalueesti"] += item["salevalueesti"]
         monthItem["m_salevalueold"] += item["salevalueold"]
         monthItem["m_salegain"] += item["salegain"]
         monthItem["m_salegainesti"] += item["salegainesti"]
         monthItem["m_salegainold"] += item["salegainold"]
         monthItem["m_tradenumber"] += item["tradenumber"]
         monthItem["m_tradenumberold"] += item["tradenumberold"]
         monthItem["m_tradeprice"] += item["tradeprice"]
         monthItem["m_tradepriceold"] += item["tradepriceold"]

         #日销售、毛利
         eitem["m_salevalue"] +=  item["salevalue"]
         eitem["m_salevalueesti"] += item["salevalueesti"]

         eitem["m_salegain"] +=  item["salegain"]
         eitem["m_salegainesti"] += item["salegainesti"]

         day1 = item["sdate"].day

         salevalue1 = "salevalue_{year}{month}{day}".format(year=year,month=month,day=day1)
         salevalueesti1 = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=day1)
         saledifference1 = "saledifference_{year}{month}{day}".format(year=year,month=month,day=day1)
         accomratio1 = "saleaccomratio_{year}{month}{day}".format(year=year,month=month,day=day1)
         eitem[salevalue1] = mtu.quantize(item["salevalue"])
         eitem[salevalueesti1] = mtu.quantize(item["salevalueesti"])
         eitem[saledifference1] = mtu.quantize(eitem[salevalue1] - eitem[salevalueesti1],"0.00",1)
         eitem[accomratio1] = mtu.convertToStr(eitem[salevalue1] * decimal.Decimal("100.0") / eitem[salevalueesti1],"0.00",1) + "%"

         salegain1 = "salegain_{year}{month}{day}".format(year=year,month=month,day=day1)
         salegainesti1 = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=day1)
         salegaindifference1 = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=day1)
         salegainaccomratio1 = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=day1)
         eitem[salegain1] = mtu.quantize(item["salegain"])
         eitem[salegainesti1] = mtu.quantize(item["salegainesti"])
         eitem[salegaindifference1] = mtu.quantize(eitem[salegain1] - eitem[salegainesti1],"0.00",1)
         eitem[salegainaccomratio1] = mtu.convertToStr(eitem[salegain1] * decimal.Decimal("100.0")/ eitem[salegainesti1],"0.00",1) + "%"

         itemShopId = item["shopid"]


     for key in mdict.keys():
         #月日均来客数 = 月累计来客数 / 天数
         item = mdict[key]
         item['m_tradenumber'] = item['m_tradenumber'] / days
         item['m_tradenumberold'] = item['m_tradenumberold'] / days
         item['m_tradeprice'] = item['m_tradeprice'] / days
         item['m_tradepriceold'] = item['m_tradepriceold'] / days

     #查询当月全月销售预算，毛利预算
     ydict = findMonthEstimate()

     for item in yearlist:
         yeardict.setdefault(item["shopid"],item)

     #全年预算
     yydict = findYearEstimate()

     #计算月累加合计
     rlist,erlist = [],[]
     sumList,esumlist ={},{}
     yearlist = []
     yearSum = {}
     sum1(slist,days,ddict,mdict,ydict,edict,rlist,sumList,erlist,esumlist,yeardict,yearlist,yearSum,yydict)

     return render(request, "report/daily/group_operate.html",{"rlist":rlist,"sumlist":sumList,"erlist":erlist,"esumlist":esumlist,"yearlist":yearlist,"yearSum":yearSum})

def sum1(slist,days,ddict,mdict,ydict,edict,rlist,sumList,rlist2,sumList2,yeardict,yearlist,yearSum,yydict):

     sumList.setdefault("sum1",{})
     sumList.setdefault("sum2",{})
     sumList.setdefault("sum3",{})
     sumList.setdefault("sum4",{})

     sumList2.setdefault("sum1",{})
     # sumList2.setdefault("sum2",{})
     sumList2.setdefault("sum3",{})
     sumList2.setdefault("sum4",{})

     yearSum.setdefault("sum1",{})
     yearSum.setdefault("sum2",{})
     yearSum.setdefault("sum3",{})
     yearSum.setdefault("sum4",{})

     today = DateUtil.get_day_of_day(-1)
     d1 = datetime.date(year = today.year,month=1,day=1)
     oldtoday = datetime.date(year = today.year-1,month=1,day=1)
     oldd1 = datetime.date(year = today.year-1,month=today.month,day=today.day)
     ydays = DateUtil.subtract(today,d1)
     ydaysold = DateUtil.subtract(oldtoday,oldd1)
     for item in slist:
         #月累计
         mergeData(item,ddict,mdict,ydict,rlist,sumList)
         #日销售、毛利
         mergeData2(item,edict,rlist2,sumList2)
         #年累计
         mergeData3(item,yeardict,yearlist,yearSum,yydict,ydays,ydaysold)

     #合计运算
     countSum(sumList,days)
     countSum2(sumList2,days)
     countSum3(yearSum)

def mergeData3(item,yeardict,yearlist,yearSum,yydict,ydays,ydaysold):
    ritem = {}
    setShopInfo(ritem,item)

    if item["shopid"] in yeardict:
         yearitem = yeardict[item["shopid"]]
    else:
         yearitem = initDayItem(item)

    ritem = dict(ritem, **yearitem)

    if item["shopid"] in yydict:
        yitem = yydict[item["shopid"]]
    else:
        yitem = initYitem(item)

    ritem = dict(ritem, **yitem)

    setYearSale(ritem,ydays,ydaysold)

     #累计求和
    setSumValue3(yearSum,ritem)

    if ritem["region"]=="13080":
         region = "承德市区"
    else:
         region = "外埠区"

    ritem["region"] = region
    yearlist.append(ritem)

def mergeData2(item,edict,rlist2,sumList2):
    year = datetime.date.today().year
    month = datetime.date.today().month
    lastDay = calendar.monthrange(year,month)[1]

    ritem = {}
    setShopInfo(ritem,item)
    if item["shopid"] in edict:
         eitem = edict[item["shopid"]]
    else:
         eitem = initEitem(item,year,month,lastDay)

    eitem["m_salevalue"] = mtu.quantize(eitem["m_salevalue"])
    eitem["m_salevalueesti"] = mtu.quantize(eitem["m_salevalueesti"])
    eitem["m_salegain"] = mtu.quantize(eitem["m_salegain"])
    eitem["m_salegainesti"] = mtu.quantize(eitem["m_salegainesti"])

    for k in eitem:
        if isinstance(eitem[k],decimal.Decimal):
            eitem[k] = float(eitem[k])


    ritem = dict(ritem, **eitem)

    #累计求和
    setSumValue2(sumList2,ritem,year,month,lastDay)

    if ritem["region"]=="13080":
         region = "承德市区"
    else:
         region = "外埠区"

    ritem["region"] = region
    rlist2.append(ritem)

def mergeData(item,ddict,mdict,ydict,rlist,sumList):
     ritem = {}
     setShopInfo(ritem,item)

     if item["shopid"] in ddict:
         dayItem = ddict[item["shopid"]]
     else:
         dayItem = initDayItem(item)
     setDaiySale(ritem,dayItem)

     if item["shopid"] in mdict:
         monthItem = mdict[item["shopid"]]
     else:
         monthItem = initMonthItem(item)

     if item["shopid"] in ydict:
         yitem = ydict[item["shopid"]]
     else:
         yitem = initYitem(item)

     setMonthSale(ritem,monthItem,yitem)

     #累计求和
     setSumValue(sumList,ritem)

     if ritem["region"]=="13080":
         region = "承德市区"
     else:
         region = "外埠区"

     ritem["region"] = region
     rlist.append(ritem)


def countSum3(sumList):
    """合计运算"""
    unkeys = ["tradenumber","tradenumberold"]
    for key in sumList.keys():
        sum = sumList[key]
        for k in sum:
            if k not in unkeys:
                sum[k] = "%0.2f" % float(sum[k])
            else:
                sum[k] = int(sum[k])

        #日销售-销售差异
        sum["sale_difference"] = str("%0.2f" % (float(sum["salevalue"])-float(sum["salevalueesti"])))
        #日销售-销售达成率
        if float(sum["salevalueesti"]) > 0:
            sum["sale_accomratio"] = str("%0.2f" % (float(sum["salevalue"])*100/float(sum["salevalueesti"])))+"%"
        else:
            sum["sale_accomratio"] = str("0.00%")
        #年销售预算季度
        if float(sum["y_salevalue"]) > 0:
            sum["sale_complet_progress"] = str("%0.2f" % (float(sum["salevalue"])*100/float(sum["y_salevalue"])))+"%"
        else:
            sum["sale_complet_progress"] = str("0.00%")
        #同比增长
        if float(sum["salevalueold"]) > 0:
            sum["sale_ynygrowth"] = str("%0.2f" % ((float(sum["salevalue"])-float(sum["salevalueold"]))*100/float(sum["salevalueold"])))+"%"
        else:
            sum["sale_ynygrowth"] = str("0.00%")

        #日销售-毛利差异
        sum["salegain_difference"] = str("%0.2f" % (float(sum["salegain"])-float(sum["salegainesti"])))

        #日销售-毛利达成率
        if float(sum["salegainesti"]) > 0:
            sum["salegain_accomratio"] = str("%0.2f" % (float(sum["salegain"])*100/float(sum["salegainesti"])))+"%"
        else:
            sum["salegain_accomratio"] = str("0.00%")
         #年毛利预算季度
        if float(sum["y_salegain"]) > 0:
            sum["salegain_complet_progress"] = str("%0.2f" % (float(sum["salegain"])*100/float(sum["y_salegain"])))+"%"
        else:
            sum["salegain_complet_progress"] = str("0.00%")
         #同比增长
        if float(sum["salegainold"]) > 0:
            sum["salegain_ynygrowth"] = str("%0.2f" % ((float(sum["salegain"])-float(sum["salegainold"]))*100/float(sum["salegainold"])))+"%"
        else:
            sum["salegain_ynygrowth"] = str("0.00%")
        #日销售-毛利毛利率
        if float(sum["salegain"]) > 0:
            sum["salegain_grossmargin"] = str("%0.2f" % (float(sum["salegain"])*100/float(sum["salevalue"])))+"%"
        else:
            sum["salegain_grossmargin"] = str("0.00%")


        #日销售-来客数同比增长
        if sum["tradenumberold"] > 0:
            sum["tradenumber_ynygrowth"] = str("%0.2f" % ((sum["tradenumber"]-sum["tradenumberold"])*100.0/sum["tradenumberold"]))+"%"
        else:
            sum["tradenumber_ynygrowth"] = str("0.00%")

        #日销售-日客单价 = 日销售实际*10000 / 日来客数
        if sum["tradenumber"] > 0:
            sum["tradeprice"] = str("%0.2f" % (float(sum["salevalue"])*10000/sum["tradenumber"]))
        else:
            sum["tradeprice"] = str("0.00")

        #日销售-去年日客单价 = 去年日销售实际*10000 / 去年日来客数
        if sum["tradenumberold"] > 0:
            sum["tradepriceold"] = str("%0.2f" % (float(sum["salevalueold"])*10000/sum["tradenumberold"]))
        else:
            sum["tradepriceold"] = str("0.00")

        #日销售-客单价同比增长
        if float(sum["tradepriceold"]) > 0:
            sum["tradeprice_ynygrowth"] = str("%0.2f" % ((float(sum["tradeprice"])-float(sum["tradepriceold"]))*100.0/float(sum["tradepriceold"])))+"%"
        else:
            sum["tradeprice_ynygrowth"] = str("0.00%")


    sumList["sum1"].setdefault("region","集团合计")
    sumList["sum2"].setdefault("region","同店合计")
    sumList["sum3"].setdefault("region","市区合计")
    sumList["sum4"].setdefault("region","外埠区合计")

def countSum2(sumList,days):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year,month)[1]

    """合计运算"""

    for key in sumList.keys():
        sum = sumList[key]
        for k in sum:
            sum[k] = "%0.2f" % float(sum[k])

        for d in range(1,lastDay+1):
            salevalue = "salevalue_{year}{month}{day}".format(year=year,month=month,day=d)
            salevalueesti = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=d)
            saledifference = "saledifference_{year}{month}{day}".format(year=year,month=month,day=d)
            saleaccomratio = "saleaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
            #差异
            sum[saledifference] = str("%0.2f" % (float(sum[salevalue])-float(sum[salevalueesti])))

            #达成率
            if float(sum[salevalueesti]) > 0:
                sum[saleaccomratio] = str("%0.2f" % (float(sum[salevalue])*100/float(sum[salevalueesti])))+"%"
            else:
                sum[saleaccomratio] = str("0.00%")

            salegain = "salegain_{year}{month}{day}".format(year=year,month=month,day=d)
            salegainesti = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=d)
            salegaindifference = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=d)
            salegainaccomratio = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)

            #差异
            sum[salegaindifference] = str("%0.2f" % (float(sum[salegain])-float(sum[salegainesti])))

            #达成率
            if float(sum[salegainesti]) > 0:
                sum[salegainaccomratio] = str("%0.2f" % (float(sum[salegain])*100/float(sum[salegainesti])))+"%"
            else:
                sum[salegainaccomratio] = str("0.00%")

    sumList["sum1"].setdefault("region","集团合计")
    # sumList["sum2"].setdefault("region","同店合计")
    sumList["sum3"].setdefault("region","市区合计")
    sumList["sum4"].setdefault("region","外埠区合计")

def countSum(sumList,days):
    """合计运算"""
    unkeys = ["day_tradenumber","day_tradenumberold","month_tradenumber","month_tradenumberold"]
    for key in sumList.keys():
        sum = sumList[key]
        for k in sum:
            if k not in unkeys:
                sum[k] = "%0.2f" % float(sum[k])
            else:
                sum[k] = int(sum[k])

        #日销售-销售差异
        sum["day_sale_difference"] = str("%0.2f" % (float(sum["day_salevalue"])-float(sum["day_salevalueesti"])))

        #日销售-销售达成率
        if float(sum["day_salevalueesti"]) > 0:
            sum["day_accomratio"] = str("%0.2f" % (float(sum["day_salevalue"])*100/float(sum["day_salevalueesti"])))+"%"
        else:
            sum["day_accomratio"] = str("0.00%")

        #日销售-来客数同比增长
        if sum["day_tradenumberold"] > 0:
            sum["day_tradenumber_ynygrowth"] = str("%0.2f" % ((sum["day_tradenumber"]-sum["day_tradenumberold"])*100.0/sum["day_tradenumberold"]))+"%"
        else:
            sum["day_tradenumber_ynygrowth"] = str("0.00%")

        #日销售-日客单价 = 日销售实际*10000 / 日来客数
        if sum["day_tradenumber"] > 0:
            sum["day_tradeprice"] = str("%0.2f" % (float(sum["day_salevalue"])*10000/sum["day_tradenumber"]))
        else:
            sum["day_tradeprice"] = str("0.00")

        #日销售-去年日客单价 = 去年日销售实际*10000 / 去年日来客数
        if sum["day_tradenumberold"] > 0:
            sum["day_tradepriceold"] = str("%0.2f" % (float(sum["day_salevalueold"])*10000/sum["day_tradenumberold"]))
        else:
            sum["day_tradepriceold"] = str("0.00")

        #日销售-客单价同比增长
        if float(sum["day_tradepriceold"]) > 0:
            sum["day_tradeprice_ynygrowth"] = str("%0.2f" % ((float(sum["day_tradeprice"])-float(sum["day_tradepriceold"]))*100.0/float(sum["day_tradepriceold"])))+"%"
        else:
            sum["day_tradeprice_ynygrowth"] = str("0.00%")

        #日销售-毛利差异
        sum["day_salegain_difference"] = str("%0.2f" % (float(sum["day_salegain"])-float(sum["day_salegainesti"])))

        #日销售-毛利达成率
        if float(sum["day_salegainesti"]) > 0:
            sum["day_salegain_accomratio"] = str("%0.2f" % (float(sum["day_salegain"])*100/float(sum["day_salegainesti"])))+"%"
        else:
            sum["day_salegain_accomratio"] = str("0.00%")

        #日销售-毛利毛利率
        if float(sum["day_salevalue"]) > 0:
            sum["day_grossmargin"] = str("%0.2f" % (float(sum["day_salegain"])*100/float(sum["day_salevalue"])))+"%"
        else:
            sum["day_grossmargin"] = str("0.00%")

        #月累计-差异
        sum["month_sale_difference"] = str("%0.2f" % (float(sum["month_salevalue"])-float(sum["month_salevalueesti"])))

        #月累计-达成率
        if float(sum["month_salevalueesti"]) > 0:
            sum["month_accomratio"] = str("%0.2f" % (float(sum["month_salevalue"])*100/float(sum["month_salevalueesti"])))+"%"
        else:
            sum["month_accomratio"] = str("0.00%")

        #月累计-月预算进度
        if float(sum["month_sale_estimate"]) > 0:
            sum["month_complet_progress"] = str("%0.2f" % (float(sum["month_salevalue"])*100/float(sum["month_sale_estimate"])))+"%"
        else:
            sum["month_complet_progress"] = str("0.00%")

        #月累计-同比增长
        if float(sum["month_salevalueold"]) > 0:
            sum["month_sale_ynygrowth"] = str("%0.2f" % ((float(sum["month_salevalue"])-float(sum["month_salevalueold"]))*100.0/float(sum["month_salevalueold"])))+"%"
        else:
            sum["month_sale_ynygrowth"] = str("0.00%")

        #月毛利-差异
        sum["month_salegain_difference"] = str("%0.2f" % (float(sum["month_salegain"])-float(sum["month_salegainesti"])))

        #月毛利-达成率
        if float(sum["month_salegainesti"]) > 0:
            sum["month_salegain_accomratio"] = str("%0.2f" % (float(sum["month_salegain"])*100/float(sum["month_salegainesti"])))+"%"
        else:
            sum["month_salegain_accomratio"] = str("0.00%")

        #月毛利-月预算进度
        if float(sum["month_salegain_estimate"]) > 0:
            sum["month_salegain_complet_progress"] = str("%0.2f" % (float(sum["month_salegain"])*100/float(sum["month_salegain_estimate"])))+"%"
        else:
            sum["month_salegain_complet_progress"] = str("0.00%")

        #月毛利-同比增长
        if float(sum["month_salevalueold"]) > 0:
            sum["month_salegain_ynygrowth"] = str("%0.2f" % ((float(sum["month_salevalue"])-float(sum["month_salevalueold"]))*100.0/float(sum["month_salevalueold"])))+"%"
        else:
            sum["month_salegain_ynygrowth"] = str("0.00%")

         #月毛利-毛利率
        if float(sum["month_salevalue"]) > 0:
            sum["month_salegain_grossmargin"] = str("%0.2f" % (float(sum["month_salegain"])*100/float(sum["month_salevalue"])))+"%"
        else:
            sum["month_salegain_grossmargin"] = str("0.00%")

        #月毛利-去年同期毛利率
        if float(sum["month_salevalueold"]) > 0:
            sum["month_salegain_grossmarginold"] = str("%0.2f" % (float(sum["month_salegainold"])*100/float(sum["month_salevalueold"])))+"%"
        else:
            sum["month_salegain_grossmarginold"] = str("0.00%")

        #月日均来客数-同比增长
        if sum["month_tradenumberold"] > 0:
            sum["month_tradenumber_ynygrowth"] = str("%0.2f" % ((sum["month_tradenumber"]-sum["month_tradenumberold"])*100.0/sum["month_tradenumberold"]))+"%"
        else:
            sum["month_tradenumber_ynygrowth"] = str("0.00%")


         #月客单价-月日均客单价=月累计销售实际 * 10000 /（月累计来客数*天数）
        if sum["month_tradenumber"] > 0:
            sum["month_tradeprice"] = str("%0.2f" % (float(sum["month_salevalue"])*10000/(sum["month_tradenumber"]*days)))
        else:
            sum["month_tradeprice"] = str("0.00")

        #月客单价-去年月日均客单价=去年月累计销售实际 * 10000 /（去年月累计来客数*天数）
        if sum["month_tradenumberold"] > 0:
            sum["month_tradepriceold"] = str("%0.2f" % (float(sum["month_salevalueold"])*10000/(sum["month_tradenumberold"]*days)))
        else:
            sum["month_tradepriceold"] = str("0.00")

        #月客单价-同比增长
        if float(sum["month_tradepriceold"]) > 0:
            sum["month_tradeprice_ynygrowth"] = str("%0.2f" % ((float(sum["month_tradeprice"])-float(sum["month_tradepriceold"]))*100.0/float(sum["month_tradepriceold"])))+"%"
        else:
            sum["month_tradeprice_ynygrowth"] = str("0.00%")

    sumList["sum1"].setdefault("region","集团合计")
    sumList["sum2"].setdefault("region","同店合计")
    sumList["sum3"].setdefault("region","市区合计")
    sumList["sum4"].setdefault("region","外埠区合计")

def setShopInfo(ritem,item):
    """设置门店信息"""
    ritem.setdefault("region",item["region"])
    ritem.setdefault("shopid",item["shopid"])
    ritem.setdefault("shopname",item["shopname"])
    ritem.setdefault("opentime",item["opentime"].strftime("%Y-%m-%d")  )
    ritem.setdefault("type",item["type"])

def setYearSale(ritem,ydays,ydaysold):
    ritem['salevalue'] = mtu.convertToStr(ritem['salevalue'],"0.00",1)
    ritem['salevalueesti'] = mtu.convertToStr(ritem['salevalueesti'],"0.00",1)
    ritem.setdefault('sale_difference',mtu.convertToStr(decimal.Decimal(ritem["salevalue"])-decimal.Decimal(ritem["salevalueesti"]),"0.00",1))
    ritem.setdefault('sale_accomratio',"{sale_accomratio}%".format(sale_accomratio=mtu.convertToStr(decimal.Decimal(ritem["salevalue"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["salevalueesti"]),"0.00",1)))

    ritem["y_salevalue"] = mtu.convertToStr(ritem['y_salevalue'],"0.00",1)
    ritem["y_salegain"] = mtu.convertToStr(ritem['y_salegain'],"0.00",1)
    ritem.setdefault('sale_complet_progress',"{sale_complet_progress}%".format(sale_complet_progress=mtu.convertToStr(decimal.Decimal(ritem["salevalue"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["y_salevalue"]),"0.00",1)))

    ritem['salevalueold'] = mtu.convertToStr(ritem['salevalueold'],"0.00",1)
    ritem.setdefault('sale_ynygrowth',mtu.convertToStr((decimal.Decimal(ritem["salevalue"])-decimal.Decimal(ritem["salevalueold"]))*decimal.Decimal("100.0")/decimal.Decimal(ritem["salevalueold"]),"0.00",1)+"%")

    ritem['salegain'] = mtu.convertToStr(ritem['salegain'],"0.00",1)
    ritem['salegainesti'] = mtu.convertToStr(ritem['salegainesti'],"0.00",1)
    ritem.setdefault('salegain_difference',mtu.convertToStr(decimal.Decimal(ritem["salegain"])-decimal.Decimal(ritem["salegainesti"]),"0.00",1))
    ritem.setdefault('salegain_accomratio',"{salegain_accomratio}%".format(salegain_accomratio=mtu.convertToStr(decimal.Decimal(ritem["salegain"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["salegainesti"]),"0.00",1)))
    ritem.setdefault('salegain_complet_progress',"{salegain_complet_progress}%".format(salegain_complet_progress=mtu.convertToStr(decimal.Decimal(ritem["salegain"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["y_salegain"]),"0.00",1)))

    ritem['salegainold'] = mtu.convertToStr(ritem['salegainold'],"0.00",1)
    ritem.setdefault('salegain_ynygrowth',mtu.convertToStr((decimal.Decimal(ritem["salegain"])-decimal.Decimal(ritem["salegainold"]))*decimal.Decimal("100.0")/decimal.Decimal(ritem["salegainold"]),"0.00",1)+"%")
    ritem.setdefault('salegain_grossmargin',"{salegain_grossmargin}%".format(salegain_grossmargin=mtu.convertToStr(decimal.Decimal(ritem["salegain"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["salevalue"]),"0.00",1)))

    #来客数
    ritem["tradenumber"] = int(ritem["tradenumber"])
    ritem["tradenumberold"] = int(ritem["tradenumberold"])
    ritem.setdefault('tradenumber_ynygrowth', mtu.convertToStr((ritem["tradenumber"]-ritem["tradenumberold"])*decimal.Decimal("100.0")/ritem["tradenumberold"],"0.00",1)+"%")

    #客单价
    ritem['tradeprice'] = mtu.convertToStr(ritem['tradeprice']/ydays,"0.00",1)
    ritem['tradepriceold'] = mtu.convertToStr(ritem['tradepriceold']/ydaysold,"0.00",1)
    ritem.setdefault('tradeprice_ynygrowth',mtu.convertToStr((decimal.Decimal(ritem["tradeprice"])-decimal.Decimal(ritem["tradepriceold"]))*decimal.Decimal("100.0")/decimal.Decimal(ritem["tradepriceold"]),"0.00",1)+"%")

    ritem["sdateold"] = str(ritem["sdateold"])

def setDaiySale(ritem,dayItem):
    """设置日运营"""
    #销售
    if dayItem["salevalue"]:
        ritem.setdefault('day_salevalue',mtu.convertToStr(dayItem['salevalue']))
    else:
       ritem.setdefault('day_salevalue',"0.00")

    if dayItem["salevalueold"]:
        ritem.setdefault('day_salevalueold',mtu.convertToStr(dayItem['salevalueold']))
    else:
       ritem.setdefault('day_salevalueold',"0.00")

    if dayItem["salevalueesti"]:
        ritem.setdefault('day_salevalueesti',mtu.convertToStr(dayItem['salevalueesti']))
    else:
        ritem.setdefault('day_salevalueesti','0.0')

    ritem.setdefault('day_sale_difference',mtu.convertToStr(mtu.quantize(dayItem["salevalue"])-mtu.quantize(dayItem["salevalueesti"]),"0.00",1))
    if dayItem["salevalueesti"]>0:
        ritem.setdefault('day_accomratio',"{day_accomratio}%".format(day_accomratio=mtu.convertToStr(mtu.quantize(dayItem["salevalue"])*decimal.Decimal("100.0")/mtu.quantize(dayItem["salevalueesti"]),"0.00",1)))
    else:
        ritem.setdefault('day_accomratio',"0.0%")

    #来客数
    if dayItem["tradenumber"]:
        ritem.setdefault('day_tradenumber',str(int(dayItem["tradenumber"])))
    else:
        ritem.setdefault('day_tradenumber',str(int(0)))

    if dayItem["tradenumberold"]:
        ritem.setdefault('day_tradenumberold',str(int(dayItem["tradenumberold"])))
    else:
        ritem.setdefault('day_tradenumberold',str(int(0)))

    if dayItem["tradenumberold"]>0:
        ritem.setdefault('day_tradenumber_ynygrowth',mtu.convertToStr((dayItem["tradenumber"]-dayItem["tradenumberold"])*decimal.Decimal("100.0")/dayItem["tradenumberold"],"0.00",1)+"%")
    else:
        ritem.setdefault('day_tradenumber_ynygrowth',"0.00")

    #客单价
    if dayItem["tradeprice"]:
        ritem.setdefault('day_tradeprice',mtu.convertToStr(dayItem['tradeprice'],"0.00",1))
    else:
        ritem.setdefault('day_tradeprice','0.00')

    if dayItem["tradepriceold"]:
        ritem.setdefault('day_tradepriceold',mtu.convertToStr(dayItem['tradepriceold'],"0.00",1))
    else:
        ritem.setdefault('day_tradepriceold', '0.00')

    if dayItem["tradeprice"] and dayItem["tradepriceold"] > 0:
        ritem.setdefault('day_tradeprice_ynygrowth',mtu.convertToStr((dayItem["tradeprice"]-dayItem["tradepriceold"])*decimal.Decimal("100.0")/dayItem["tradepriceold"],"0.00",1)+"%")
    else:
        ritem.setdefault('day_tradeprice_ynygrowth',"0.00")

    #毛利
    if dayItem["salegain"]:
        ritem.setdefault('day_salegain',mtu.convertToStr(dayItem['salegain']))
    else:
        ritem.setdefault('day_salegain',"0.0")

    if dayItem["salegainesti"]:
        ritem.setdefault('day_salegainesti',mtu.convertToStr(dayItem['salegainesti']))
    else:
        ritem.setdefault('day_salegainesti',"0.0")

    ritem.setdefault('day_salegain_difference',mtu.convertToStr(mtu.quantize(dayItem["salegain"])-mtu.quantize(dayItem["salegainesti"]),"0.00",1))

    if dayItem["salegainesti"] > 0:
        ritem.setdefault('day_salegain_accomratio',mtu.convertToStr(mtu.quantize(dayItem["salegain"])*decimal.Decimal("100.0")/mtu.quantize(dayItem["salegainesti"]),"0.00",1)+"%")
    else:
        ritem.setdefault('day_salegain_accomratio',"0.00")

    if dayItem["salevalue"] > 0:
        ritem.setdefault('day_grossmargin',mtu.convertToStr(mtu.quantize(dayItem["salegain"])*decimal.Decimal("100.0")/mtu.quantize(dayItem["salevalue"]),"0.00",1)+"%")
    else:
        ritem.setdefault('day_grossmargin',"0.00")

def setMonthSale(ritem,monthItem,yitem):
    """设置月运营"""
    #月累计销售额
    if monthItem["m_salevalue"]:
        ritem.setdefault('month_salevalue',mtu.convertToStr(monthItem["m_salevalue"]))
    else:
        ritem.setdefault('month_salevalue', "0.0")

    if monthItem["m_salevalueesti"]:
        ritem.setdefault('month_salevalueesti',mtu.convertToStr(monthItem["m_salevalueesti"]))
    else:
        ritem.setdefault('month_salevalueesti',"0.0")


    ritem.setdefault('month_sale_difference',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"])-mtu.quantize(monthItem["m_salevalueesti"]),"0.00",1))

    if monthItem["m_salevalueesti"]:
        ritem.setdefault('month_accomratio',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"])*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalueesti"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_accomratio',"0.00")

    if yitem["y_salevalue"]:
        ritem.setdefault('month_sale_estimate',mtu.convertToStr(yitem['y_salevalue']))
    else:
        ritem.setdefault('month_sale_estimate',"0.0")

    if yitem["y_salevalue"] > 0:
        ritem.setdefault('month_complet_progress',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"])*decimal.Decimal("100.0")/mtu.quantize(yitem["y_salevalue"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_complet_progress',"0.00")

    if monthItem["m_salevalueold"]:
        ritem.setdefault('month_salevalueold',mtu.convertToStr(monthItem["m_salevalueold"]))
    else:
        ritem.setdefault('month_salevalueold',"0.0")

    if monthItem["m_salevalueold"] > 0:
        ritem.setdefault('month_sale_ynygrowth',mtu.convertToStr((mtu.quantize(monthItem["m_salevalue"])-mtu.quantize(monthItem["m_salevalueold"]))*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalueold"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_sale_ynygrowth',"0.00")
    #月毛利
    if monthItem["m_salegain"]:
        ritem.setdefault('month_salegain',mtu.convertToStr(monthItem["m_salegain"]))
    else:
        ritem.setdefault('month_salegain',"0.0")

    if monthItem["m_salegainesti"]:
        ritem.setdefault('month_salegainesti',mtu.convertToStr(monthItem["m_salegainesti"]))
    else:
        ritem.setdefault('month_salegainesti',"0.0")

    ritem.setdefault('month_salegain_difference',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"])-mtu.quantize(monthItem["m_salegainesti"]),"0.00",1))

    if monthItem["m_salegainesti"] > 0:
        ritem.setdefault('month_salegain_accomratio',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"])*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salegainesti"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_accomratio',"0.00")

    if yitem["y_salegain"]:
        ritem.setdefault('month_salegain_estimate',mtu.convertToStr(yitem['y_salegain']))
    else:
        ritem.setdefault('month_salegain_estimate',"0.0")

    if yitem["y_salegain"] > 0:
        ritem.setdefault('month_salegain_complet_progress',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"])*decimal.Decimal("100.0")/mtu.quantize(yitem["y_salegain"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_complet_progress',"0.00")

    if monthItem["m_salegainold"]:
        ritem.setdefault('month_salegainold',mtu.convertToStr(monthItem["m_salegainold"]))
    else:
        ritem.setdefault('month_salegainold',"0.0")

    if monthItem["m_salegainold"] > 0:
        ritem.setdefault('month_salegain_ynygrowth',mtu.convertToStr((mtu.quantize(monthItem["m_salegain"]) - mtu.quantize(monthItem["m_salegainold"]))*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salegainold"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_ynygrowth',"0.00")

    if monthItem["m_salevalue"] > 0:
        ritem.setdefault('month_salegain_grossmargin',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"])*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalue"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_grossmargin',"0.00")

    if monthItem["m_salevalueold"] > 0:
        ritem.setdefault('month_salegain_grossmarginold',mtu.convertToStr(mtu.quantize(monthItem["m_salegainold"])*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalueold"]),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_grossmarginold',"0.00")

    #月日均来客数
    if monthItem["m_tradenumber"]:
        ritem.setdefault('month_tradenumber',str(int(monthItem["m_tradenumber"])))
    else:
        ritem.setdefault('month_tradenumber',"0")

    if monthItem["m_tradenumberold"]:
        ritem.setdefault('month_tradenumberold',str(int(monthItem["m_tradenumberold"])))
    else:
        ritem.setdefault('month_tradenumberold',"0")

    if monthItem["m_tradenumberold"] > 0:
        ritem.setdefault('month_tradenumber_ynygrowth',mtu.convertToStr((monthItem["m_tradenumber"]-monthItem["m_tradenumberold"])*decimal.Decimal("100.0")/monthItem["m_tradenumberold"],"0.00",1)+"%")
    else:
        ritem.setdefault('month_tradenumber_ynygrowth',"0.00")

    #月客单价
    if monthItem["m_tradeprice"]:
        ritem.setdefault('month_tradeprice',mtu.convertToStr(monthItem["m_tradeprice"],'0.00',1))
    else:
        ritem.setdefault('month_tradeprice',"0.00")

    if monthItem["m_tradepriceold"]:
        ritem.setdefault('month_tradepriceold',mtu.convertToStr(monthItem["m_tradepriceold"],'0.00',1))
    else:
        ritem.setdefault('month_tradepriceold',"0.00")

    if monthItem["m_tradepriceold"] > 0:
        ritem.setdefault('month_tradeprice_ynygrowth',mtu.convertToStr((monthItem["m_tradeprice"]-monthItem["m_tradepriceold"])*decimal.Decimal("100.0")/monthItem["m_tradepriceold"],"0.00",1)+"%")
    else:
        ritem.setdefault('month_tradeprice_ynygrowth',"0.00")

def setSumValue(sumList,ritem):
    """ 计算合计 """
    #集团合计
    setValue(sumList["sum1"],ritem)
    #同店合计
    if ritem["type"] == "同店":
        setValue(sumList["sum2"],ritem)

    if ritem["region"]=="13080":
        #市区合计
        setValue(sumList["sum3"],ritem)
    else:
        #外埠区合计
        setValue(sumList["sum4"],ritem)

def setSumValue2(sumList,ritem,year,month,lastDay):
    """ 计算合计 """
    #集团合计
    setValue2(sumList["sum1"],ritem,year,month,lastDay)
    #同店合计
    # if ritem["type"] == "同店":
    #     setValue2(sumList["sum2"],ritem,year,month,lastDay)

    if ritem["region"]=="13080":
        #市区合计
        setValue2(sumList["sum3"],ritem,year,month,lastDay)
    else:
        #外埠区合计
        setValue2(sumList["sum4"],ritem,year,month,lastDay)

def setSumValue3(sumList,ritem):
    """ 计算合计 """
    #集团合计
    setValue3(sumList["sum1"],ritem)
    #同店合计
    if ritem["type"] == "同店":
        setValue3(sumList["sum2"],ritem)

    if ritem["region"]=="13080":
        #市区合计
        setValue3(sumList["sum3"],ritem)
    else:
        #外埠区合计
        setValue3(sumList["sum4"],ritem)

def setValue3(sum1,ritem):
   if "salevalue" in sum1:
       sum1["salevalue"] = str(float(sum1["salevalue"]) + float(ritem["salevalue"]))
   else:
       sum1["salevalue"] = str(float(ritem["salevalue"]))

   if "salevalueold" in sum1:
       sum1["salevalueold"] = str(float(sum1["salevalueold"]) + float(ritem["salevalueold"]))
   else:
       sum1["salevalueold"] = str(float(ritem["salevalueold"]))

   if "salevalueesti" in sum1:
       sum1["salevalueesti"] = str(float(sum1["salevalueesti"]) + float(ritem["salevalueesti"]))
   else:
       sum1["salevalueesti"] = str(float(ritem["salevalueesti"]))

   if "tradenumber" in sum1:
       sum1["tradenumber"] = str(int(sum1["tradenumber"]) + int(ritem["tradenumber"]))
   else:
       sum1["tradenumber"] = str(int(ritem["tradenumber"]))

   if "tradenumberold" in sum1:
       sum1["tradenumberold"] = str(int(sum1["tradenumberold"]) + int(ritem["tradenumberold"]))
   else:
       sum1["tradenumberold"] = str(int(ritem["tradenumberold"]))

   if "salegain" in sum1:
       sum1["salegain"] = str(float(sum1["salegain"]) + float(ritem["salegain"]))
   else:
       sum1["salegain"] = str(float(ritem["salegain"]))

   if "salegainold" in sum1:
       sum1["salegainold"] = str(float(sum1["salegainold"]) + float(ritem["salegainold"]))
   else:
       sum1["salegainold"] = str(float(ritem["salegainold"]))

   if "salegainesti" in sum1:
       sum1["salegainesti"] = str(float(sum1["salegainesti"]) + float(ritem["salegainesti"]))
   else:
       sum1["salegainesti"] = str(float(ritem["salegainesti"]))

   if "y_salevalue" in sum1:
       sum1["y_salevalue"] = str(float(sum1["y_salevalue"]) + float(ritem["y_salevalue"]))
   else:
       sum1["y_salevalue"] = str(float(ritem["y_salevalue"]))

   if "y_salegain" in sum1:
       sum1["y_salegain"] = str(float(sum1["y_salegain"]) + float(ritem["y_salegain"]))
   else:
       sum1["y_salegain"] = str(float(ritem["y_salegain"]))


def setValue2(sum1,ritem,year,month,lastDay):
    if "m_salevalue" in sum1:
        sum1["m_salevalue"] = str(float(sum1["m_salevalue"]) + float(ritem["m_salevalue"]))
    else:
        sum1["m_salevalue"] = str(float(ritem["m_salevalue"]))

    if "m_salevalueesti" in sum1:
        sum1["m_salevalueesti"] = str(float(sum1["m_salevalueesti"]) + float(ritem["m_salevalueesti"]))
    else:
        sum1["m_salevalueesti"] = str(float(ritem["m_salevalueesti"]))

    if "m_salegain" in sum1:
        sum1["m_salegain"] = str(float(sum1["m_salegain"]) + float(ritem["m_salegain"]))
    else:
        sum1["m_salegain"] = str(float(ritem["m_salegain"]))

    if "m_salegainesti" in sum1:
        sum1["m_salegainesti"] = str(float(sum1["m_salegainesti"]) + float(ritem["m_salegainesti"]))
    else:
        sum1["m_salegainesti"] = str(float(ritem["m_salegainesti"]))

    for d in range(1,lastDay+1):
        salevalue = "salevalue_{year}{month}{day}".format(year=year,month=month,day=d)
        salevalueesti = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=d)
        salegain = "salegain_{year}{month}{day}".format(year=year,month=month,day=d)
        salegainesti = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=d)

        if salevalue in sum1:
            sum1[salevalue] = str(float(sum1[salevalue]) + float(ritem[salevalue]))
        else:
            sum1[salevalue] = str(float(ritem[salevalue]))

        if salevalueesti in sum1:
            sum1[salevalueesti] = str(float(sum1[salevalueesti]) + float(ritem[salevalueesti]))
        else:
            sum1[salevalueesti] = str(float(ritem[salevalueesti]))

        if salegain in sum1:
            sum1[salegain] = str(float(sum1[salegain]) + float(ritem[salegain]))
        else:
            sum1[salegain] = str(float(ritem[salegain]))

        if salegainesti in sum1:
            sum1[salegainesti] = str(float(sum1[salegainesti]) + float(ritem[salegainesti]))
        else:
            sum1[salegainesti] = str(float(ritem[salegainesti]))

def setValue(sum1,ritem):
   if "day_salevalue" in sum1:
       sum1["day_salevalue"] = str(float(sum1["day_salevalue"]) + float(ritem["day_salevalue"]))
   else:
       sum1["day_salevalue"] = str(float(ritem["day_salevalue"]))

   if "day_salevalueold" in sum1:
       sum1["day_salevalueold"] = str(float(sum1["day_salevalueold"]) + float(ritem["day_salevalueold"]))
   else:
       sum1["day_salevalueold"] = str(float(ritem["day_salevalueold"]))

   if "day_salevalueesti" in sum1:
       sum1["day_salevalueesti"] = str(float(sum1["day_salevalueesti"]) + float(ritem["day_salevalueesti"]))
   else:
       sum1["day_salevalueesti"] = str(float(ritem["day_salevalueesti"]))

   if "day_tradenumber" in sum1:
       sum1["day_tradenumber"] = str(int(sum1["day_tradenumber"]) + int(ritem["day_tradenumber"]))
   else:
       sum1["day_tradenumber"] = str(int(ritem["day_tradenumber"]))

   if "day_tradenumberold" in sum1:
       sum1["day_tradenumberold"] = str(int(sum1["day_tradenumberold"]) + int(ritem["day_tradenumberold"]))
   else:
       sum1["day_tradenumberold"] = str(int(ritem["day_tradenumberold"]))

   if "day_salegain" in sum1:
       sum1["day_salegain"] = str(float(sum1["day_salegain"]) + float(ritem["day_salegain"]))
   else:
       sum1["day_salegain"] = str(float(ritem["day_salegain"]))

   if "day_salegainesti" in sum1:
       sum1["day_salegainesti"] = str(float(sum1["day_salegainesti"]) + float(ritem["day_salegainesti"]))
   else:
       sum1["day_salegainesti"] = str(float(ritem["day_salegainesti"]))

   if "month_salevalue" in sum1:
       sum1["month_salevalue"] = str(float(sum1["month_salevalue"]) + float(ritem["month_salevalue"]))
   else:
       sum1["month_salevalue"] = str(float(ritem["month_salevalue"]))

   if "month_salevalueesti" in sum1:
       sum1["month_salevalueesti"] = str(float(sum1["month_salevalueesti"]) + float(ritem["month_salevalueesti"]))
   else:
       sum1["month_salevalueesti"] = str(float(ritem["month_salevalueesti"]))

   if "month_sale_estimate" in sum1:
       sum1["month_sale_estimate"] = str(float(sum1["month_sale_estimate"]) + float(ritem["month_sale_estimate"]))
   else:
       sum1["month_sale_estimate"] = str(float(ritem["month_sale_estimate"]))

   if "month_salevalueold" in sum1:
       sum1["month_salevalueold"] = str(float(sum1["month_salevalueold"]) + float(ritem["month_salevalueold"]))
   else:
       sum1["month_salevalueold"] = str(float(ritem["month_salevalueold"]))

   if "month_salegain" in sum1:
       sum1["month_salegain"] = str(float(sum1["month_salegain"]) + float(ritem["month_salegain"]))
   else:
       sum1["month_salegain"] = str(float(ritem["month_salegain"]))

   if "month_salegainesti" in sum1:
       sum1["month_salegainesti"] = str(float(sum1["month_salegainesti"]) + float(ritem["month_salegainesti"]))
   else:
       sum1["month_salegainesti"] = str(float(ritem["month_salegainesti"]))

   if "month_salegain_estimate" in sum1:
       sum1["month_salegain_estimate"] = str(float(sum1["month_salegain_estimate"]) + float(ritem["month_salegain_estimate"]))
   else:
       sum1["month_salegain_estimate"] = str(float(ritem["month_salegain_estimate"]))

   if "month_salegainold" in sum1:
       sum1["month_salegainold"] = str(float(sum1["month_salegainold"]) + float(ritem["month_salegainold"]))
   else:
       sum1["month_salegainold"] = str(float(ritem["month_salegainold"]))

   if "month_tradenumber" in sum1:
       sum1["month_tradenumber"] = str(int(sum1["month_tradenumber"]) + int(ritem["month_tradenumber"]))
   else:
       sum1["month_tradenumber"] = str(int(ritem["month_tradenumber"]))

   if "month_tradenumberold" in sum1:
       sum1["month_tradenumberold"] = str(int(sum1["month_tradenumberold"]) + int(ritem["month_tradenumberold"]))
   else:
       sum1["month_tradenumberold"] = str(int(ritem["month_tradenumberold"]))


def findYearEstimate():
     edict = {}
     date = DateUtil.get_day_of_day(-1)
     year = date.year
     start = (datetime.datetime(year,1,1)).strftime("%Y%m%d")
     yesterday = date.strftime("%Y%m%d")

     karrs = {}
     karrs.setdefault("shopid__contains","C")
     karrs.setdefault("dateid__gte","{start}".format(start=start))
     karrs.setdefault("dateid__lte","{end}".format(end=yesterday))
     elist = Estimate.objects.values("shopid")\
                     .filter(**karrs).order_by("shopid")\
                     .annotate(y_salevalue=Sum('salevalue')/10000,y_salegain=Sum('salegain')/10000)

     for item in elist:
         edict.setdefault(str(item["shopid"]),item)

     return edict

def findMonthEstimate():
     month = datetime.date.today().month
     edict = {}
     karrs = {}
     karrs.setdefault("shopid__contains","C")
     karrs.setdefault("dateid__month","{month}".format(month=month))
     elist = Estimate.objects.values("shopid")\
                     .filter(**karrs)\
                     .annotate(y_salevalue=Sum('salevalue'),y_salegain=Sum('salegain'))

     for item in elist:
         edict.setdefault(str(item["shopid"]),item)

     return edict

def initEitem(item,year,month,lastDay):
   eitem = {}
   eitem.setdefault("shopid",item["shopid"])
   for d in range(1,lastDay+1):
        salevalue = "salevalue_{year}{month}{day}".format(year=year,month=month,day=d)
        salevalueesti = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=d)
        saledifference = "saledifference_{year}{month}{day}".format(year=year,month=month,day=d)
        accomratio = "saleaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
        eitem.setdefault(salevalue,0.0)
        eitem.setdefault(salevalueesti,0.0)
        eitem.setdefault(saledifference,0.0)
        eitem.setdefault(accomratio,"0.0%")

        salegain = "salegain_{year}{month}{day}".format(year=year,month=month,day=d)
        salegainesti = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=d)
        salegaindifference = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=d)
        salegainaccomratio = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
        eitem.setdefault(salegain,0.0)
        eitem.setdefault(salegainesti,0.0)
        eitem.setdefault(salegaindifference,0.0)
        eitem.setdefault(salegainaccomratio,"0.0%")
   return eitem

def initDayItem(item):
    dayItem = {}
    dayItem.setdefault("shopid",item["shopid"])
    dayItem.setdefault('salevalue',0.00)
    dayItem.setdefault('salevalueold',0.00)
    dayItem.setdefault('salevalueesti',0.00)
    dayItem.setdefault('tradenumber',0)
    dayItem.setdefault('tradenumberold',0)
    dayItem.setdefault('tradeprice',0.00)
    dayItem.setdefault('tradepriceold',0.00)
    dayItem.setdefault('salegain',0.00)
    dayItem.setdefault('salegainesti',0.00)
    return dayItem

def initMonthItem(item):
    monthItem = {}
    monthItem.setdefault("shopid",item["shopid"])
    monthItem.setdefault("m_salevalue",0.00)
    monthItem.setdefault("m_salevalueesti",0.00)
    monthItem.setdefault("m_salevalueold",0.00)
    monthItem.setdefault("m_salegain",0.00)
    monthItem.setdefault("m_salegainesti",0.00)
    monthItem.setdefault("m_salegainold",0.00)
    monthItem.setdefault("m_tradenumber",0)
    monthItem.setdefault("m_tradenumberold",0)
    monthItem.setdefault("m_tradeprice",0.00)
    monthItem.setdefault("m_tradepriceold",0.00)
    return monthItem

def initYitem(item):
    eitem = {}
    eitem.setdefault("shopid",item["shopid"])
    eitem.setdefault("y_salegain",0.00)
    eitem.setdefault("y_salevalue",0.00)
    return eitem

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass