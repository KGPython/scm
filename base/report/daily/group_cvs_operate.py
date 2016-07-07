#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum,Avg
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import Kshopsale,BasShopRegion,Estimate,BasPurLog
from django.http import HttpResponse
import datetime,calendar,decimal
import xlwt3 as xlwt

@csrf_exempt
def index(request):
     karrs = {}

     date = DateUtil.get_day_of_day(-1)
     days = date.day
     year = date.year
     month = date.month

     oldyesterday = datetime.date(year=date.year - 1, month=date.month, day=date.day)
     oldstart = datetime.date(year=date.year - 1, month=1, day=1)

     start = (date.replace(day=1)).strftime("%Y-%m-%d")
     yesterday = date.strftime("%Y-%m-%d")
     lastDay = calendar.monthrange(year,month)[1]

     #查询所有超市门店
     slist = BasShopRegion.objects.values("shopid","shopname","region","opentime","type").filter(shoptype=13).order_by("region","shopid")
     shopids = [ shop["shopid"] for shop in slist]

     #查询当月销售
     karrs.setdefault("sdate__gte","{start} 00:00:00".format(start=start))
     karrs.setdefault("sdate__lte","{end} 23:59:59".format(end=yesterday))
     karrs.setdefault("shopid__in",shopids)
     baselist = Kshopsale.objects.values('shopid','sdate','salevalue','salegain','tradenumber','tradeprice','salevalueesti','salegainesti',
                                         'tradenumberold','tradepriceold','salevalueold','salegainold').filter(**karrs).order_by("shopid")

     karrs.clear()
     karrs.setdefault("sdate__year","{year}".format(year=year))
     karrs.setdefault("shopid__in",shopids)
     yearlist = Kshopsale.objects.values("shopid")\
                     .filter(**karrs).order_by("shopid")\
                     .annotate(salevalue=Sum('salevalue'),salegain=Sum('salegain'),tradenumber=Sum('tradenumber')
                                              ,tradeprice=Sum('tradeprice'),salevalueesti=Sum('salevalueesti')
                                              ,salegainesti=Sum('salegainesti')
                                              ,tradenumberold=Sum('tradenumberold'),tradepriceold=Sum('tradepriceold')
                                              ,salevalueold=Sum('salevalueold'),salegainold=Sum('salegainold'))

     avglist = Kshopsale.objects.values("shopid") \
         .filter(**karrs).order_by("shopid") \
         .annotate(tradenumber_avg=Avg('tradenumber'))

     avgdict = {aitem["shopid"]: aitem["tradenumber_avg"] for aitem in avglist}

     karrs.clear()
     karrs.setdefault("sdateold__gte", "{start} 00:00:00".format(start=oldstart))
     karrs.setdefault("sdateold__lte", "{end} 23:59:59".format(end=oldyesterday))
     karrs.setdefault("shopid__in", shopids)
     oldavglist = Kshopsale.objects.values("shopid") \
         .filter(**karrs).order_by("shopid") \
         .annotate(tradenumberold_avg=Avg('tradenumberold'))
     oldavgdict = {aitem["shopid"]: aitem["tradenumberold_avg"] for aitem in oldavglist}

     yearavglist = []
     for shop in slist:
         vagItem = {}
         shopid = shop["shopid"]
         vagItem.setdefault("shopid", shopid)
         if shopid in avgdict:
             vagItem.setdefault("tradenumber_avg", avgdict[shopid])
         else:
             vagItem.setdefault("tradenumber_avg", decimal.Decimal("0"))

         if shopid in oldavgdict:
             vagItem.setdefault("tradenumberold_avg", oldavgdict[shopid])
         else:
             vagItem.setdefault("tradenumberold_avg", decimal.Decimal("0"))
         yearavglist.append(vagItem)


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
                eitem.setdefault(salevalue,decimal.Decimal("0.00"))
                eitem.setdefault(salevalueesti,decimal.Decimal("0.00"))
                eitem.setdefault(saledifference,decimal.Decimal("0.00"))
                eitem.setdefault(accomratio,"0.0%")

                salegain = "salegain_{year}{month}{day}".format(year=year,month=month,day=d)
                salegainesti = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=d)
                salegaindifference = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=d)
                salegainaccomratio = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
                eitem.setdefault(salegain,decimal.Decimal("0.00"))
                eitem.setdefault(salegainesti,decimal.Decimal("0.00"))
                eitem.setdefault(salegaindifference,decimal.Decimal("0.00"))
                eitem.setdefault(salegainaccomratio,"0.0%")

            edict.setdefault(shopid,eitem)

         #月累计
         if  item["salevalue"]:
            monthItem["m_salevalue"] += item["salevalue"]
         if item["salevalueesti"]:
            monthItem["m_salevalueesti"] += item["salevalueesti"]
         if item["salevalueold"]:
            monthItem["m_salevalueold"] += item["salevalueold"]
         if item["salegain"]:
            monthItem["m_salegain"] += item["salegain"]
         if item["salegainesti"]:
            monthItem["m_salegainesti"] += item["salegainesti"]
         if  item["salegainold"]:
            monthItem["m_salegainold"] += item["salegainold"]
         if item["tradenumber"]:
            monthItem["m_tradenumber"] += item["tradenumber"]
         if item["tradenumberold"]:
            monthItem["m_tradenumberold"] += item["tradenumberold"]

         # if item["tradeprice"]:
         #    monthItem["m_tradeprice"] += item["tradeprice"]
         # if item["tradepriceold"]:
         #    monthItem["m_tradepriceold"] += item["tradepriceold"]

         #日销售、毛利
         if item["salevalue"]:
            eitem["m_salevalue"] +=  item["salevalue"]
         if item["salevalueesti"]:
            eitem["m_salevalueesti"] += item["salevalueesti"]
         if  item["salegain"]:
            eitem["m_salegain"] +=  item["salegain"]
         if item["salegainesti"]:
            eitem["m_salegainesti"] += item["salegainesti"]

         day1 = item["sdate"].day

         salevalue1 = "salevalue_{year}{month}{day}".format(year=year,month=month,day=day1)
         salevalueesti1 = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=day1)
         saledifference1 = "saledifference_{year}{month}{day}".format(year=year,month=month,day=day1)
         accomratio1 = "saleaccomratio_{year}{month}{day}".format(year=year,month=month,day=day1)
         eitem[salevalue1] = mtu.quantize(item["salevalue"],"0.00",1)
         eitem[salevalueesti1] = mtu.quantize(item["salevalueesti"],"0.00",1)
         eitem[saledifference1] = mtu.quantize(eitem[salevalue1] - eitem[salevalueesti1],"0.00",1)
         if eitem[salevalueesti1] > 0:
            eitem[accomratio1] = mtu.convertToStr(eitem[salevalue1] * decimal.Decimal("100.0") / eitem[salevalueesti1],"0.00",1) + "%"
         else:
            eitem[accomratio1] = ""

         salegain1 = "salegain_{year}{month}{day}".format(year=year,month=month,day=day1)
         salegainesti1 = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=day1)
         salegaindifference1 = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=day1)
         salegainaccomratio1 = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=day1)
         eitem[salegain1] = mtu.quantize(item["salegain"],"0.00",1)
         eitem[salegainesti1] = mtu.quantize(item["salegainesti"],"0.00",1)
         eitem[salegaindifference1] = mtu.quantize(eitem[salegain1] - eitem[salegainesti1],"0.00",1)
         if eitem[salegainesti1]>0:
            eitem[salegainaccomratio1] = mtu.convertToStr(eitem[salegain1] * decimal.Decimal("100.0")/ eitem[salegainesti1],"0.00",1) + "%"
         else:
            eitem[salegainaccomratio1] = ""

         itemShopId = item["shopid"]


     for key in mdict.keys():
         #月日均来客数 = 月累计来客数 / 天数
         item = mdict[key]
         item['m_tradenumber'] = mtu.quantize(item['m_tradenumber'] / days,"0",1)
         item['m_tradenumberold'] =  mtu.quantize(item['m_tradenumberold'] / oldyesterday.day,"0",1)

         if item['m_tradenumber'] > 0:
            item['m_tradeprice'] = item['m_salevalue'] /days / item['m_tradenumber']
         if item['m_tradenumberold'] > 0:
            item['m_tradepriceold'] = item['m_salevalueold'] /days / item['m_tradenumberold']

     #查询当月全月销售预算，毛利预算
     ydict = findMonthEstimate(shopids)

     for item in yearlist:
         yeardict.setdefault(item["shopid"],item)

     yearavgdict = {}
     for item in yearavglist:
         yearavgdict.setdefault(item["shopid"],item)


     #全年预算
     yydict = findYearEstimate(shopids)

     #计算月累加合计
     rlist,erlist = [],[]
     sumDict,esumDict ={},{}
     yearlist = []
     yearSumDict = {}
     sum1(slist,days,ddict,mdict,ydict,edict,rlist,sumDict,
          erlist,esumDict,yeardict,yearlist,yearSumDict,yydict,yearavgdict,date)

     qtype = mtu.getReqVal(request,"qtype","1")

     #操作日志
     if not qtype:
         qtype = "1"
     key_state = mtu.getReqVal(request, "key_state", '')
     if qtype == '2' and (not key_state or key_state != '2'):
         qtype = '1'
     path = request.path
     today = datetime.datetime.today();
     ucode = request.session.get("s_ucode")
     uname = request.session.get("s_uname")
     BasPurLog.objects.create(name="便利店销售日报",url=path,qtype=qtype,ucode=ucode,uname=uname,createtime=today)

     if qtype == "1":
         return render(request, "report/daily/group_cvs_operate.html",{"rlist":rlist,"sumlist":sumDict,"erlist":erlist,"esumlist":esumDict,"yearlist":yearlist,"yearSum":yearSumDict})
     else:
         return export(rlist,sumDict,erlist,esumDict,yearlist,yearSumDict)



def sum1(slist,days,ddict,mdict,ydict,edict,rlist,sumDict,rlist2,sumDict2,yeardict,yearlist,yearSumDict,yydict,yearavgdict,yestoday):

     sumDict.setdefault("sum1",{})
     sumDict.setdefault("sum2",{})

     sumDict2.setdefault("sum1",{})

     yearSumDict.setdefault("sum1",{})
     yearSumDict.setdefault("sum2",{})

     for item in slist:
         #月累计
         mergeData(item,ddict,mdict,ydict,rlist,sumDict)
         #日销售、毛利
         mergeData2(item,edict,rlist2,sumDict2,yestoday)
         #年累计
         mergeData3(item,yeardict,yearlist,yearSumDict,yydict,yearavgdict)

     #合计运算
     countSum(sumDict,days)
     countSum2(sumDict2)
     countSum3(yearSumDict)

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

     if ritem["region"]=="13083":
         region = "便利店"
     else:
        region = ""

     ritem["region"] = region
     rlist.append(ritem)

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

        #日销售-日客单价 = 日销售实际* / 日来客数
        if sum["day_tradenumber"] > 0:
            sum["day_tradeprice"] = str("%0.2f" % (float(sum["day_salevalue"])/sum["day_tradenumber"]))
        else:
            sum["day_tradeprice"] = str("0.00")

        #日销售-去年日客单价 = 去年日销售实际 / 去年日来客数
        if sum["day_tradenumberold"] > 0:
            sum["day_tradepriceold"] = str("%0.2f" % (float(sum["day_salevalueold"])/sum["day_tradenumberold"]))
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


         #月客单价-月日均客单价=月累计销售实际  /（月累计来客数*天数）
        if sum["month_tradenumber"] > 0:
            sum["month_tradeprice"] = str("%0.2f" % (float(sum["month_salevalue"])/(sum["month_tradenumber"]*days)))
        else:
            sum["month_tradeprice"] = str("0.00")

        #月客单价-去年月日均客单价=去年月累计销售实际  /（去年月累计来客数*天数）
        if sum["month_tradenumberold"] > 0:
            sum["month_tradepriceold"] = str("%0.2f" % (float(sum["month_salevalueold"])/(sum["month_tradenumberold"]*days)))
        else:
            sum["month_tradepriceold"] = str("0.00")

        #月客单价-同比增长
        if float(sum["month_tradepriceold"]) > 0:
            sum["month_tradeprice_ynygrowth"] = str("%0.2f" % ((float(sum["month_tradeprice"])-float(sum["month_tradepriceold"]))*100.0/float(sum["month_tradepriceold"])))+"%"
        else:
            sum["month_tradeprice_ynygrowth"] = str("0.00%")

    sumList["sum1"].setdefault("region","便利店全部合计")
    sumList["sum2"].setdefault("region","同店合计")


def setShopInfo(ritem,item):
    """设置门店信息"""
    ritem.setdefault("region",item["region"])
    ritem.setdefault("shopid",item["shopid"])
    ritem.setdefault("shopname",item["shopname"])
    if item["opentime"]:
        ritem.setdefault("opentime",item["opentime"].strftime("%Y-%m-%d"))
    else:
        ritem.setdefault("opentime","")
    ritem.setdefault("type",item["type"])


def setDaiySale(ritem,dayItem):
    """设置日运营"""
    #销售
    ritem.setdefault('day_salevalue',mtu.convertToStr(dayItem['salevalue'],"0.00",1))
    ritem.setdefault('day_salevalueold',mtu.convertToStr(dayItem['salevalueold'],"0.00",1))
    ritem.setdefault('day_salevalueesti',mtu.convertToStr(dayItem['salevalueesti'],"0.00",1))

    ritem.setdefault('day_sale_difference',mtu.convertToStr(mtu.quantize(dayItem["salevalue"],"0.00",1)-mtu.quantize(dayItem["salevalueesti"],"0.00",1),"0.00",1))
    if mtu.quantize(dayItem["salevalueesti"],"0.00",1)>0:
        ritem.setdefault('day_accomratio',"{day_accomratio}%".format(day_accomratio=mtu.convertToStr(mtu.quantize(dayItem["salevalue"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(dayItem["salevalueesti"],"0.00",1),"0.00",1)))
    else:
        ritem.setdefault('day_accomratio',"0.0%")

    #来客数
    if dayItem["tradenumber"]:
        ritem.setdefault('day_tradenumber',int(dayItem["tradenumber"]))
    else:
        ritem.setdefault('day_tradenumber',0)
    if dayItem['tradenumberold']:
        ritem.setdefault('day_tradenumberold',int(dayItem["tradenumberold"]))
    else:
        ritem.setdefault('day_tradenumberold',0)

    if dayItem["tradenumberold"]>0:
        ritem.setdefault('day_tradenumber_ynygrowth',mtu.convertToStr((dayItem["tradenumber"]-dayItem["tradenumberold"])*decimal.Decimal("100.0")/dayItem["tradenumberold"],"0.00",1)+"%")
    else:
        ritem.setdefault('day_tradenumber_ynygrowth',"0.00")

    #客单价
    ritem.setdefault('day_tradeprice',mtu.convertToStr(dayItem['tradeprice'],"0.00",1))
    ritem.setdefault('day_tradepriceold',mtu.convertToStr(dayItem['tradepriceold'],"0.00",1))

    if  dayItem["tradepriceold"] > 0:
        ritem.setdefault('day_tradeprice_ynygrowth',mtu.convertToStr((dayItem["tradeprice"]-dayItem["tradepriceold"])*decimal.Decimal("100.0")/dayItem["tradepriceold"],"0.00",1)+"%")
    else:
        ritem.setdefault('day_tradeprice_ynygrowth',"0.00")

    #毛利
    ritem.setdefault('day_salegain',mtu.convertToStr(dayItem['salegain'],"0.00",1))
    ritem.setdefault('day_salegainesti',mtu.convertToStr(dayItem['salegainesti'],"0.00",1))
    ritem.setdefault('day_salegain_difference',mtu.convertToStr(mtu.quantize(dayItem["salegain"],"0.00",1)-mtu.quantize(dayItem["salegainesti"],"0.00",1),"0.00",1))

    if mtu.quantize(dayItem["salegainesti"],"0.00",1) > 0:
        ritem.setdefault('day_salegain_accomratio',mtu.convertToStr(mtu.quantize(dayItem["salegain"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(dayItem["salegainesti"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('day_salegain_accomratio',"0.00")

    if mtu.quantize(dayItem["salevalue"],"0.00",1) > 0:
        ritem.setdefault('day_grossmargin',mtu.convertToStr(mtu.quantize(dayItem["salegain"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(dayItem["salevalue"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('day_grossmargin',"0.00")

def setSumValue(sumList,ritem):
    """ 计算合计 """
    #集团合计
    setValue(sumList["sum1"],ritem)
    #同店合计
    if ritem["type"] == "同店":
        setValue(sumList["sum2"],ritem)
def setValue(sum1,ritem):
   if "day_salevalue" in sum1:
       sum1["day_salevalue"] = str(float(sum1["day_salevalue"]) + float(ritem["day_salevalue"]))
   else:
       sum1["day_salevalue"] = ritem["day_salevalue"]

   if "day_salevalueold" in sum1:
       sum1["day_salevalueold"] = str(float(sum1["day_salevalueold"]) + float(ritem["day_salevalueold"]))
   else:
       sum1["day_salevalueold"] = ritem["day_salevalueold"]

   if "day_salevalueesti" in sum1:
       sum1["day_salevalueesti"] = str(float(sum1["day_salevalueesti"]) + float(ritem["day_salevalueesti"]))
   else:
       sum1["day_salevalueesti"] = ritem["day_salevalueesti"]

   if "day_tradenumber" in sum1:
       sum1["day_tradenumber"] = sum1["day_tradenumber"] + ritem["day_tradenumber"]
   else:
       sum1["day_tradenumber"] = ritem["day_tradenumber"]

   if "day_tradenumberold" in sum1:
       sum1["day_tradenumberold"] = sum1["day_tradenumberold"] + ritem["day_tradenumberold"]
   else:
       sum1["day_tradenumberold"] = ritem["day_tradenumberold"]

   if "day_salegain" in sum1:
       sum1["day_salegain"] = str(float(sum1["day_salegain"]) + float(ritem["day_salegain"]))
   else:
       sum1["day_salegain"] = ritem["day_salegain"]

   if "day_salegainesti" in sum1:
       sum1["day_salegainesti"] = str(float(sum1["day_salegainesti"]) + float(ritem["day_salegainesti"]))
   else:
       sum1["day_salegainesti"] = ritem["day_salegainesti"]

   if "month_salevalue" in sum1:
       sum1["month_salevalue"] = str(float(sum1["month_salevalue"]) + float(ritem["month_salevalue"]))
   else:
       sum1["month_salevalue"] = ritem["month_salevalue"]

   if "month_salevalueesti" in sum1:
       sum1["month_salevalueesti"] = str(float(sum1["month_salevalueesti"]) + float(ritem["month_salevalueesti"]))
   else:
       sum1["month_salevalueesti"] = ritem["month_salevalueesti"]

   if "month_sale_estimate" in sum1:
       sum1["month_sale_estimate"] = str(float(sum1["month_sale_estimate"]) + float(ritem["month_sale_estimate"]))
   else:
       sum1["month_sale_estimate"] = ritem["month_sale_estimate"]

   if "month_salevalueold" in sum1:
       sum1["month_salevalueold"] = str(float(sum1["month_salevalueold"]) + float(ritem["month_salevalueold"]))
   else:
       sum1["month_salevalueold"] = ritem["month_salevalueold"]

   if "month_salegain" in sum1:
       sum1["month_salegain"] = str(float(sum1["month_salegain"]) + float(ritem["month_salegain"]))
   else:
       sum1["month_salegain"] = ritem["month_salegain"]

   if "month_salegainesti" in sum1:
       sum1["month_salegainesti"] = str(float(sum1["month_salegainesti"]) + float(ritem["month_salegainesti"]))
   else:
       sum1["month_salegainesti"] = ritem["month_salegainesti"]

   if "month_salegain_estimate" in sum1:
       sum1["month_salegain_estimate"] = str(float(sum1["month_salegain_estimate"]) + float(ritem["month_salegain_estimate"]))
   else:
       sum1["month_salegain_estimate"] = ritem["month_salegain_estimate"]

   if "month_salegainold" in sum1:
       sum1["month_salegainold"] = str(float(sum1["month_salegainold"]) + float(ritem["month_salegainold"]))
   else:
       sum1["month_salegainold"] = ritem["month_salegainold"]

   if "month_tradenumber" in sum1:
       sum1["month_tradenumber"] = sum1["month_tradenumber"] + ritem["month_tradenumber"]
   else:
       sum1["month_tradenumber"] = ritem["month_tradenumber"]

   if "month_tradenumberold" in sum1:
       sum1["month_tradenumberold"] = sum1["month_tradenumberold"]+ ritem["month_tradenumberold"]
   else:
       sum1["month_tradenumberold"] = ritem["month_tradenumberold"]

def setMonthSale(ritem,monthItem,yitem):
    """设置月运营"""
    #月累计销售额
    ritem.setdefault('month_salevalue',mtu.convertToStr(monthItem["m_salevalue"],"0.00",1))
    ritem.setdefault('month_salevalueesti',mtu.convertToStr(monthItem["m_salevalueesti"],"0.00",1))

    ritem.setdefault('month_sale_difference',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"],"0.00",1)-mtu.quantize(monthItem["m_salevalueesti"],"0.00",1),"0.00",1))

    if monthItem["m_salevalueesti"] > 0:
        ritem.setdefault('month_accomratio',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalueesti"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_accomratio',"0.00")

    ritem.setdefault('month_sale_estimate',mtu.convertToStr(yitem['y_salevalue'],"0.00",1))

    if yitem["y_salevalue"] > 0:
        ritem.setdefault('month_complet_progress',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(yitem["y_salevalue"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_complet_progress',"0.00")

    ritem.setdefault('month_salevalueold',mtu.convertToStr(monthItem["m_salevalueold"],"0.00",1))

    if monthItem["m_salevalueold"] > 0:
        ritem.setdefault('month_sale_ynygrowth',mtu.convertToStr((mtu.quantize(monthItem["m_salevalue"],"0.00",1)-mtu.quantize(monthItem["m_salevalueold"],"0.00",1))*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalueold"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_sale_ynygrowth',"0.00")
    #月毛利
    ritem.setdefault('month_salegain',mtu.convertToStr(monthItem["m_salegain"],"0.00",1))

    ritem.setdefault('month_salegainesti',mtu.convertToStr(monthItem["m_salegainesti"],"0.00",1))

    ritem.setdefault('month_salegain_difference',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"],"0.00",1)-mtu.quantize(monthItem["m_salegainesti"],"0.00",1),"0.00",1))

    if monthItem["m_salegainesti"] > 0:
        ritem.setdefault('month_salegain_accomratio',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salegainesti"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_accomratio',"0.00")

    ritem.setdefault('month_salegain_estimate',mtu.convertToStr(yitem['y_salegain'],"0.00",1))

    if yitem["y_salegain"] > 0:
        ritem.setdefault('month_salegain_complet_progress',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(yitem["y_salegain"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_complet_progress',"0.00")

    ritem.setdefault('month_salegainold',mtu.convertToStr(monthItem["m_salegainold"],"0.00",1))

    if monthItem["m_salegainold"] > 0:
        ritem.setdefault('month_salegain_ynygrowth',mtu.convertToStr((mtu.quantize(monthItem["m_salegain"],"0.00",1) - mtu.quantize(monthItem["m_salegainold"],"0.00",1))*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salegainold"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_ynygrowth',"0.00")

    if monthItem["m_salevalue"] > 0:
        ritem.setdefault('month_salegain_grossmargin',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalue"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_grossmargin',"0.00")

    if monthItem["m_salevalueold"] > 0:
        ritem.setdefault('month_salegain_grossmarginold',mtu.convertToStr(mtu.quantize(monthItem["m_salegainold"],"0.00",1)*decimal.Decimal("100.0")/mtu.quantize(monthItem["m_salevalueold"],"0.00",1),"0.00",1)+"%")
    else:
        ritem.setdefault('month_salegain_grossmarginold',"0.00")

    #月日均来客数
    ritem.setdefault('month_tradenumber',int(monthItem["m_tradenumber"]))
    ritem.setdefault('month_tradenumberold',int(monthItem["m_tradenumberold"]))

    if monthItem["m_tradenumberold"] > 0:
        ritem.setdefault('month_tradenumber_ynygrowth',mtu.convertToStr((monthItem["m_tradenumber"]-monthItem["m_tradenumberold"])*decimal.Decimal("100.0")/monthItem["m_tradenumberold"],"0.00",1)+"%")
    else:
        ritem.setdefault('month_tradenumber_ynygrowth',"0.00")

    #月客单价
    ritem.setdefault('month_tradeprice',mtu.convertToStr(monthItem["m_tradeprice"],'0.00',1))
    ritem.setdefault('month_tradepriceold',mtu.convertToStr(monthItem["m_tradepriceold"],'0.00',1))

    if monthItem["m_tradepriceold"] > 0:
        ritem.setdefault('month_tradeprice_ynygrowth',mtu.convertToStr((monthItem["m_tradeprice"]-monthItem["m_tradepriceold"])*decimal.Decimal("100.0")/monthItem["m_tradepriceold"],"0.00",1)+"%")
    else:
        ritem.setdefault('month_tradeprice_ynygrowth',"0.00")


def mergeData2(item,edict,rlist2,sumList2,yestoday):
    year = yestoday.year
    month = yestoday.month
    lastDay = calendar.monthrange(year,month)[1]

    ritem = {}
    setShopInfo(ritem,item)
    if item["shopid"] in edict:
         eitem = edict[item["shopid"]]
    else:
         eitem = initEitem(item,year,month,lastDay)

    eitem["m_salevalue"] = mtu.quantize(eitem["m_salevalue"],"0.00",1)
    eitem["m_salevalueesti"] = mtu.quantize(eitem["m_salevalueesti"],"0.00",1)
    eitem["m_salegain"] = mtu.quantize(eitem["m_salegain"],"0.00",1)
    eitem["m_salegainesti"] = mtu.quantize(eitem["m_salegainesti"],"0.00",1)

    for k in eitem:
        if isinstance(eitem[k],decimal.Decimal):
            eitem[k] = float(eitem[k])


    ritem = dict(ritem, **eitem)

    #累计求和
    setSumValue2(sumList2,ritem,year,month,lastDay)

    if ritem["region"]=="13083":
         region = "便利店"
    else:
        region = ""

    ritem["region"] = region
    rlist2.append(ritem)


def findMonthEstimate(shopids):
     date = DateUtil.get_day_of_day(-1)
     month = date.month
     edict = {}
     karrs = {}
     karrs.setdefault("shopid__in",shopids)
     karrs.setdefault("dateid__month","{month}".format(month=month))
     elist = Estimate.objects.values("shopid")\
                     .filter(**karrs)\
                     .annotate(y_salevalue=Sum('salevalue'),y_salegain=Sum('salegain'))

     for item in elist:
         edict.setdefault(str(item["shopid"]),item)

     return edict

def setSumValue2(sumList,ritem,year,month,lastDay):
    """ 计算合计 """
    setValue2(sumList["sum1"],ritem,year,month,lastDay)



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

def countSum2(sumList):
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

    sumList["sum1"].setdefault("region","便利店全部合计")


def mergeData3(item,yeardict,yearlist,yearSum,yydict,yearavgdict):
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

    setYearSale(ritem,yearavgdict)

     #累计求和
    setSumValue3(yearSum,ritem)

    if ritem["region"]=="13083":
         region = "便利店"
    else:
        region = ""

    ritem["region"] = region
    yearlist.append(ritem)


def setYearSale(ritem,yearavgdict):
    ritem['salevalue'] = mtu.convertToStr(ritem['salevalue'],"0.00",1)
    ritem['salevalueesti'] = mtu.convertToStr(ritem['salevalueesti'],"0.00",1)
    ritem.setdefault('sale_difference',mtu.convertToStr(decimal.Decimal(ritem["salevalue"])-decimal.Decimal(ritem["salevalueesti"]),"0.00",1))
    if decimal.Decimal(ritem["salevalueesti"]) > 0:
        ritem.setdefault('sale_accomratio',"{sale_accomratio}%".format(sale_accomratio=mtu.convertToStr(decimal.Decimal(ritem["salevalue"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["salevalueesti"]),"0.00",1)))
    else:
        ritem.setdefault('sale_accomratio',"")

    ritem["y_salevalue"] = mtu.convertToStr(ritem['y_salevalue'],"0.00",1)
    ritem["y_salegain"] = mtu.convertToStr(ritem['y_salegain'],"0.00",1)
    if decimal.Decimal(ritem["y_salevalue"]) > 0:
        ritem.setdefault('sale_complet_progress',"{sale_complet_progress}%".format(sale_complet_progress=mtu.convertToStr(decimal.Decimal(ritem["salevalue"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["y_salevalue"]),"0.00",1)))
    else:
        ritem.setdefault('sale_complet_progress',"")

    ritem['salevalueold'] = mtu.convertToStr(ritem['salevalueold'],"0.00",1)

    if decimal.Decimal(ritem["salevalueold"]) > 0:
        ritem.setdefault('sale_ynygrowth',mtu.convertToStr((decimal.Decimal(ritem["salevalue"])-decimal.Decimal(ritem["salevalueold"]))*decimal.Decimal("100.0")/decimal.Decimal(ritem["salevalueold"]),"0.00",1)+"%")
    else:
       ritem.setdefault('sale_ynygrowth',"");

    ritem['salegain'] = mtu.convertToStr(ritem['salegain'],"0.00",1)
    ritem['salegainesti'] = mtu.convertToStr(ritem['salegainesti'],"0.00",1)
    ritem.setdefault('salegain_difference',mtu.convertToStr(decimal.Decimal(ritem["salegain"])-decimal.Decimal(ritem["salegainesti"]),"0.00",1))
    if decimal.Decimal(ritem["salegainesti"]) > 0:
        ritem.setdefault('salegain_accomratio',"{salegain_accomratio}%".format(salegain_accomratio=mtu.convertToStr(decimal.Decimal(ritem["salegain"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["salegainesti"]),"0.00",1)))
    else:
        ritem.setdefault('salegain_accomratio',"")

    if decimal.Decimal(ritem["y_salegain"]) > 0:
        ritem.setdefault('salegain_complet_progress',"{salegain_complet_progress}%".format(salegain_complet_progress=mtu.convertToStr(decimal.Decimal(ritem["salegain"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["y_salegain"]),"0.00",1)))
    else:
        ritem.setdefault('salegain_complet_progress',"")

    ritem['salegainold'] = mtu.convertToStr(ritem['salegainold'],"0.00",1)
    if decimal.Decimal(ritem["salegainold"]) > 0:
        ritem.setdefault('salegain_ynygrowth',mtu.convertToStr((decimal.Decimal(ritem["salegain"])-decimal.Decimal(ritem["salegainold"]))*decimal.Decimal("100.0")/decimal.Decimal(ritem["salegainold"]),"0.00",1)+"%")
    else:
        ritem.setdefault('salegain_ynygrowth',"")

    if decimal.Decimal(ritem["salevalue"]) > 0:
        ritem.setdefault('salegain_grossmargin',"{salegain_grossmargin}%".format(salegain_grossmargin=mtu.convertToStr(decimal.Decimal(ritem["salegain"])*decimal.Decimal("100.0")/decimal.Decimal(ritem["salevalue"]),"0.00",1)))
    else:
        ritem.setdefault('salegain_grossmargin',"")


     #客单价 = 总销售 / 总客流
    if  ritem["tradenumber"] and ritem["tradenumber"] > 0:
        ritem['tradeprice'] = mtu.convertToStr(decimal.Decimal(ritem["salevalue"])/ritem["tradenumber"],"0.00",1)
    else:
        ritem['tradeprice'] = "0.00"

    if ritem["tradenumberold"] and ritem["tradenumberold"] > 0:
        ritem['tradepriceold'] = mtu.convertToStr(decimal.Decimal(ritem["salevalueold"])/ritem["tradenumberold"],"0.00",1)
    else:
        ritem["tradepriceold"] = "0.00"
    #累计来客数
    ritem.setdefault("tradenumber_total",int("%0.0f" % ritem['tradenumber']))
    ritem.setdefault("tradenumberold_total",int("%0.0f" % ritem['tradenumberold']))

    #来客数 = 总客流 / 天数
    if ritem["shopid"] in yearavgdict:
        numitem = yearavgdict[ritem["shopid"]]
        ritem["tradenumber"] = int("%0.0f" % numitem['tradenumber_avg'])
        ritem["tradenumberold"] = int("%0.0f" % numitem['tradenumberold_avg'])
    else:
        ritem["tradenumber"] = 0
        ritem["tradenumberold"] = 0

    if ritem["tradenumberold"] > 0:
        ritem.setdefault('tradenumber_ynygrowth', mtu.convertToStr((ritem["tradenumber"]-ritem["tradenumberold"])*decimal.Decimal("100.0")/ritem["tradenumberold"],"0.00",1)+"%")
    else:
        ritem.setdefault('tradenumber_ynygrowth',"")

    #日均来客数
    # ritem["tradenumber"] = "%0.0f" % numitem['tradenumber_avg']
    # ritem["tradenumberold"] = "%0.0f" % numitem['tradenumberold_avg']

def setSumValue3(sumList,ritem):
    """ 计算合计 """
    setValue3(sumList["sum1"],ritem)
    #同店合计
    if ritem["type"] == "同店":
        setValue3(sumList["sum2"],ritem)


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
       sum1["tradenumber"] = sum1["tradenumber"] + ritem["tradenumber"]
   else:
       sum1["tradenumber"] = ritem["tradenumber"]

   if "tradenumberold" in sum1:
       sum1["tradenumberold"] = sum1["tradenumberold"] + ritem["tradenumberold"]
   else:
       sum1["tradenumberold"] = ritem["tradenumberold"]

   if "tradenumber_total" in sum1:
       sum1["tradenumber_total"] = sum1["tradenumber_total"] + ritem["tradenumber_total"]
   else:
       sum1["tradenumber_total"] = ritem["tradenumber_total"]

   if "tradenumberold_total" in sum1:
       sum1["tradenumberold_total"] = sum1["tradenumberold_total"] + ritem["tradenumberold_total"]
   else:
       sum1["tradenumberold_total"] = ritem["tradenumberold_total"]

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



def countSum3(sumList):
    """合计运算"""
    unkeys = ["tradenumber","tradenumberold","tradenumber_total","tradenumberold_total"]
    for key in sumList.keys():
        sum = sumList[key]
        for k in sum:
            if k not in unkeys:
                sum[k] = "%0.2f" % float(sum[k])
            else:
                sum[k] = sum[k]

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

        #日销售-日客单价 = 日销售实际 / 日来客数
        if sum["tradenumber_total"] > 0:
            sum["tradeprice"] = str("%0.2f" % (float(sum["salevalue"])/sum["tradenumber"]))
        else:
            sum["tradeprice"] = str("0.00")

        #日销售-去年日客单价 = 去年日销售实际 / 去年日来客数
        if sum["tradenumberold_total"] > 0:
            sum["tradepriceold"] = str("%0.2f" % (float(sum["salevalueold"])/sum["tradenumberold"]))
        else:
            sum["tradepriceold"] = str("0.00")

        #日销售-客单价同比增长
        if float(sum["tradepriceold"]) > 0:
            sum["tradeprice_ynygrowth"] = str("%0.2f" % ((float(sum["tradeprice"])-float(sum["tradepriceold"]))*100.0/float(sum["tradepriceold"])))+"%"
        else:
            sum["tradeprice_ynygrowth"] = str("0.00%")


    sumList["sum1"].setdefault("region","便利店全部合计")
    sumList["sum2"].setdefault("region","同店合计")


def findYearEstimate(shopids):
     edict = {}
     date = DateUtil.get_day_of_day(-1)
     year = date.year

     karrs = {}
     karrs.setdefault("shopid__in",shopids)
     karrs.setdefault("dateid__year",year)
     elist = Estimate.objects.values("shopid")\
                     .filter(**karrs).order_by("shopid")\
                     .annotate(y_salevalue=Sum('salevalue'),y_salegain=Sum('salegain'))

     for item in elist:
         edict.setdefault(str(item["shopid"]),item)

     return edict

def initEitem(item,year,month,lastDay):
   eitem = {}
   eitem.setdefault("shopid",item["shopid"])
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
    dayItem.setdefault('salegainold',0.00)
    dayItem.setdefault('salegainesti',0.00)
    return dayItem

def initMonthItem(item):
    monthItem = {}
    monthItem.setdefault("shopid",item["shopid"])
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
    return monthItem

def initYitem(item):
    eitem = {}
    eitem.setdefault("shopid",item["shopid"])
    eitem.setdefault("y_salegain",0.00)
    eitem.setdefault("y_salevalue",0.00)
    return eitem

def export(rlist,sumList,erlist,esumlist,yearlist,yearSum):

    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)

    #写入sheet1 月累计销售报表
    writeDataToSheet1(wb,rlist,sumList)
    #写入sheet2 （月）日销售报表、（月）日毛利报表
    writeDataToSheet2(wb,erlist,esumlist)
    #写入sheet4 年累计销售报表
    writeDataToSheet3(wb,yearlist,yearSum)

    date = DateUtil.get_day_of_day(-1)
    outtype = 'application/vnd.ms-excel;'
    fname = date.strftime("%m.%d")+"grp_daily_cvs_opt"

    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response

def writeDataToSheet1(wb,rlist,sumDict):
    date = DateUtil.get_day_of_day(-1)
    days = date.day
    year = date.year
    month = date.month
    yesterday = date.strftime("%Y-%m-%d")
    lastDay = calendar.monthrange(year,month)[1]

    sheet = wb.add_sheet("月累计销售报表",cell_overwrite_ok=True)
    #月时间进度
    progress = "%0.2f" % (days * 100.0/lastDay)

    titles = [[("（%s月）日销售报表" % month,0,1,15)],
              [("数据日期：",0,1,2),(yesterday,2,1,1),("月时间进度：",5,1,1),("{progress}%".format(progress=progress),6,1,1),("单位：元",21,1,1)],
              [("区域",0,3,1),("店号",1,3,1),("店名",2,3,1),("开业时间",3,3,1),("类型",4,3,1),("当日销售",5,1,15),("月累计销售额",20,1,8),
               ("月毛利",28,1,10),("月日均来客数",38,1,3),("月客单价",41,1,3)],
              [("销售",5,1,4),("来客数",9,1,3),("客单价",12,1,3),("毛利",15,1,5),("实际",20,2,1),("预算",21,2,1),("差异",22,2,1),
               ("达成率",23,2,1),("全月预算",24,2,1),("月预算进度",25,2,1),("去年销售",26,2,1),("同比增长",27,2,1),
               ("实际",28,2,1),("预算",29,2,1),("差异",30,2,1),("达成率",31,2,1),("全月预算",32,2,1),("月预算进度",33,2,1),("去年同期",34,2,1),
               ("同比增长",35,2,1),("毛利率",36,2,1),("去年同期毛利率",37,2,1),("月累计来客数",38,2,1),("去年",39,2,1),("同比增长",40,2,1),
               ("月累计客单价",41,2,1),("去年",42,2,1),("同比增长",43,2,1)],
              [("实际",5,1,1),("预算",6,1,1),("差异",7,1,1),("达成率",8,1,1),("当日",9,1,1),("去年",10,1,1),("同比增长",11,1,1)
               ,("当日",12,1,1),("去年",13,1,1),("同比增长",14,1,1),("毛利额",15,1,1),("预算",16,1,1),("差异",17,1,1),("达成率",18,1,1)
               ,("毛利率",19,1,1)]
            ]

    keylist = ['region','shopid','shopname','opentime','type','day_salevalue','day_salevalueesti','day_sale_difference','day_accomratio',
               'day_tradenumber','day_tradenumberold','day_tradenumber_ynygrowth','day_tradeprice','day_tradepriceold','day_tradeprice_ynygrowth',
               'day_salegain','day_salegainesti','day_salegain_difference','day_salegain_accomratio','day_grossmargin','month_salevalue'
               ,'month_salevalueesti','month_sale_difference','month_accomratio','month_sale_estimate','month_complet_progress','month_salevalueold',
               'month_sale_ynygrowth','month_salegain','month_salegainesti','month_salegain_difference','month_salegain_accomratio','month_salegain_estimate',
               'month_salegain_complet_progress','month_salegainold','month_salegain_ynygrowth','month_salegain_grossmargin','month_salegain_grossmarginold',
               'month_tradenumber','month_tradenumberold','month_tradenumber_ynygrowth','month_tradeprice','month_tradepriceold','month_tradeprice_ynygrowth']

    widthList = [600,400,1000,800,400,800,800,800,800,800,800,800,800,800,800,800,800,800,800,800,
                 800,800,800,800,800,800,800,800,800,800,800,800,800,800,800,800,800,1200,800,800,
                 800,800,800,800]

    mtu.insertTitle2(sheet,titles,keylist,widthList)
    #合计["","","","",sum1,sum2,sum3]   ["key1","key2","key3","key4"...]
    count = mtu.insertSum2(sheet,keylist,5,sumDict,5)
    #数据 [{"key":value,"key":value},{},...]   ["key1","key2","key3","key4"...]
    #dictlist code 转 name 字典 [{"key":value,"key":value},{},...]
    mtu.insertCell2(sheet,count,rlist,keylist,None)

def writeDataToSheet2(wb,erlist,esumDict):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year,month)[1]

    sheet = wb.add_sheet("（月）日销售报表",cell_overwrite_ok=True)
    sheet2 = wb.add_sheet("（月）日毛利报表",cell_overwrite_ok=True)

    titles = [[("（%s月）日销售报表" % month,0,1,15)],
              [("区域",0,2,1),("店号",1,2,1),("店名",2,2,1),("开业时间",3,2,1),("类型",4,2,1),("累计实际",5,2,1),("累计预算",6,2,1)],
              []]

    titles2 = [[("（%s月）日毛利报表" % month,0,1,15)],
              [("区域",0,2,1),("店号",1,2,1),("店名",2,2,1),("开业时间",3,2,1),("类型",4,2,1),("月累计毛利",5,2,1),("月累计预算",6,2,1)],
              []]

    keylist = ['region','shopid','shopname','opentime','type','m_salevalue','m_salevalueesti']
    keylist2 = ['region','shopid','shopname','opentime','type','m_salegain','m_salegainesti']

    widthList = [600,400,1000,800,400,800,800]

    trow1 = titles[1]
    trow2 = titles[2]

    trow3 = titles2[1]
    trow4 = titles2[2]

    n = 7
    for d in range(1,lastDay+1):
        salevalue = "salevalue_{year}{month}{day}".format(year=year,month=month,day=d)
        salevalueesti = "salevalueesti_{year}{month}{day}".format(year=year,month=month,day=d)
        saledifference = "saledifference_{year}{month}{day}".format(year=year,month=month,day=d)
        accomratio = "saleaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
        keylist.append(salevalue)
        keylist.append(salevalueesti)
        keylist.append(saledifference)
        keylist.append(accomratio)

        salegain = "salegain_{year}{month}{day}".format(year=year,month=month,day=d)
        salegainesti = "salegainesti_{year}{month}{day}".format(year=year,month=month,day=d)
        salegaindifference = "salegaindifference_{year}{month}{day}".format(year=year,month=month,day=d)
        salegainaccomratio = "salegainaccomratio_{year}{month}{day}".format(year=year,month=month,day=d)
        keylist2.append(salegain)
        keylist2.append(salegainesti)
        keylist2.append(salegaindifference)
        keylist2.append(salegainaccomratio)

        t1 = ("{month}月{day}日".format(month=month,day=d),n,1,4)
        trow1.append(t1)
        trow3.append(t1)

        widthList.append(800)
        widthList.append(800)
        widthList.append(800)
        widthList.append(800)

        t21 = ('实际',n,1,1)
        t22 = ('预算',n+1,1,1)
        t23 = ('差异',n+2,1,1)
        t24 = ('达成率',n+3,1,1)
        trow2.append(t21)
        trow2.append(t22)
        trow2.append(t23)
        trow2.append(t24)

        trow4.append(t21)
        trow4.append(t22)
        trow4.append(t23)
        trow4.append(t24)

        n += 4
    #日销售报表
    mtu.insertTitle2(sheet,titles,keylist,widthList)
    count = mtu.insertSum2(sheet,keylist,3,esumDict,5)
    mtu.insertCell2(sheet,count,erlist,keylist,None)
    #日毛利报表
    mtu.insertTitle2(sheet2,titles2,keylist2,widthList)
    count2 = mtu.insertSum2(sheet2,keylist2,3,esumDict,5)
    mtu.insertCell2(sheet2,count2,erlist,keylist2,None)

def writeDataToSheet3(wb,yearlist,yearSumDict):
    date = DateUtil.get_day_of_day(-1)
    days = date.day
    year = date.year
    month = date.month
    yesterday = date.strftime("%Y-%m-%d")
    lastDay = calendar.monthrange(year,month)[1]

    sheet = wb.add_sheet("年累计销售报表",cell_overwrite_ok=True)
    #月时间进度
    progress = "%0.2f" % (days * 100.0/lastDay)

    titles = [[("年累计销售报表",0,1,15)],
              [("数据日期：",0,1,2),(yesterday,2,1,1),("月时间进度：",5,1,1),("{progress}%".format(progress=progress),6,1,1),("单位：元",8,1,1)],
              [("区域",0,2,1),("店号",1,2,1),("店名",2,2,1),("开业时间",3,2,1),("类型",4,2,1),("年累计销售额",5,1,8),("年累计毛利",13,1,9),
               ("年日均来客数",22,1,3),("年日均客单价",25,1,3)],
              [("实际",5,2,1),("累计预算",6,2,1),("差异",7,2,1),("达成率",8,2,1),("全年预算",9,2,1),("年预算进度",10,2,1),
               ("去年",11,2,1),("同比增长",12,2,1),("实际",13,2,1),("累计预算",14,2,1),("差异",15,2,1),("达成率",16,2,1),("全年预算",17,2,1),
               ("年预算进度",18,2,1),("去年",19,2,1),("同比增长",20,2,1),("毛利率",21,2,1),("实际",22,2,1),("去年",23,2,1),("同比增长",24,2,1),
               ("年累计",25,2,1),("去年",26,2,1),("同比增长",27,2,1)],
            ]

    keylist = ['region','shopid','shopname','opentime','type','salevalue','salevalueesti','sale_difference','sale_accomratio',
               'y_salevalue','sale_complet_progress','salevalueold','sale_ynygrowth','salegain','salegainesti',
               'salegain_difference','salegain_accomratio','y_salegain','salegain_complet_progress','salegainold','salegain_ynygrowth'
               ,'salegain_grossmargin','tradenumber','tradenumberold','tradenumber_ynygrowth','tradeprice','tradepriceold',
               'tradeprice_ynygrowth']

    widthList = [600,400,1000,800,400,800,800,800,800,800,800,800,800,800,800,800,800,800,800,800,
                 800,800,800,800,800,800,800,800]

    mtu.insertTitle2(sheet,titles,keylist,widthList)
    count = mtu.insertSum2(sheet,keylist,4,yearSumDict,5)
    mtu.insertCell2(sheet,count,yearlist,keylist,None)