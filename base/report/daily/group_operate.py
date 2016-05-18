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
     start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
     yesterday = DateUtil.get_day_of_day(-2).strftime("%Y-%m-%d")
     days = DateUtil.get_day_of_day(-2).day

     #查询所有超市门店
     slist = BasShopRegion.objects.values("shopid","shopname","region","opentime","type").order_by("region","shopid")

     #查询当日销售
     karrs.setdefault("sdate__gte","{start} 00:00:00".format(start=yesterday))
     karrs.setdefault("sdate__lte","{end} 23:59:59".format(end=yesterday))
     dlist = Kshopsale.objects.values("sdate","shopid","salevalue","salegain","tradenumber","tradeprice",
                                      "salevalueesti","salegainesti","sdateold","tradenumberold",
                                      "tradepriceold","salevalueold","salegainold").filter(**karrs).order_by("shopid")
     ddict = {}
     for item in dlist:
         ddict.setdefault(str(item["shopid"]),item)

     #查询当月销售
     karrs.clear()
     karrs.setdefault("sdate__gte","{start} 00:00:00".format(start=start))
     karrs.setdefault("sdate__lte","{end} 23:59:59".format(end=yesterday))
     mlist = Kshopsale.objects.values("shopid")\
                     .filter(**karrs)\
                     .annotate(m_salevalue=Sum('salevalue'),m_salegain=Sum('salegain'),m_tradenumber=Sum('tradenumber')
                                              ,m_tradeprice=Sum('tradeprice'),m_salevalueesti=Sum('salevalueesti')
                                              ,m_salegainesti=Sum('salegainesti'),m_sdateold=Sum('sdateold')
                                              ,m_tradenumberold=Sum('tradenumberold'),m_tradepriceold=Sum('tradepriceold')
                                              ,m_salevalueold=Sum('salevalueold'),m_salegainold=Sum('salegainold'))

     mdict = {}
     for item in mlist:
         #月日均来客数 = 月累计来客数 / 天数
         item['m_tradenumber'] = item['m_tradenumber'] / days
         item['m_tradenumberold'] = item['m_tradenumberold'] / days
         item['m_tradeprice'] = item['m_tradeprice'] / days
         item['m_tradepriceold'] = item['m_tradepriceold'] / days
         mdict.setdefault(str(item["shopid"]),item)

     #查询当月全月销售预算，毛利预算
     start = (datetime.date.today().replace(day=1)).strftime("%Y%m%d")
     year = datetime.date.today().year
     month = datetime.date.today().month
     d = calendar.monthrange(year,month)
     end = (datetime.date.today().replace(day=d[1])).strftime("%Y%m%d")
     karrs.clear()
     karrs.setdefault("shopid__contains","C")
     karrs.setdefault("dateid__gte","{start}".format(start=start))
     karrs.setdefault("dateid__lte","{end}".format(end=end))
     elist = Estimate.objects.values("shopid")\
                     .filter(**karrs)\
                     .annotate(y_salevalue=Sum('salevalue'),y_salegain=Sum('salegain'))
     edict = {}
     for item in elist:
         edict.setdefault(str(item["shopid"]),item)

     rlist = []
     sumList ={}
     sum1,sum2,sum3,sum4 = {},{},{},{}

     sumList.setdefault("sum1",sum1)
     sumList.setdefault("sum2",sum2)
     sumList.setdefault("sum3",sum3)
     sumList.setdefault("sum4",sum4)

     for item in slist:
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

         if item["shopid"] in edict:
             eitem = edict[item["shopid"]]
         else:
             eitem = initEitem(item)

         setMonthSale(ritem,monthItem,eitem)

         #累计求和
         setSumValue(sumList,ritem)

         if ritem["region"]=="13080":
             region = "承德市区"
         else:
             region = "外埠区"

         ritem["region"] = region
         rlist.append(ritem)

     #合计运算
     countSum(sumList,days)

     return render(request, "report/daily/group_operate.html",{"rlist":rlist,"sumlist":sumList})

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

def initEitem(item):
    eitem = {}
    eitem.setdefault("shopid",item["shopid"])
    eitem.setdefault("y_salegain",0.00)
    eitem.setdefault("y_salevalue",0.00)
    return eitem

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

def setMonthSale(ritem,monthItem,eitem):
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

    if eitem["y_salevalue"]:
        ritem.setdefault('month_sale_estimate',mtu.convertToStr(eitem['y_salevalue']))
    else:
        ritem.setdefault('month_sale_estimate',"0.0")

    if eitem["y_salevalue"] > 0:
        ritem.setdefault('month_complet_progress',mtu.convertToStr(mtu.quantize(monthItem["m_salevalue"])*decimal.Decimal("100.0")/mtu.quantize(eitem["y_salevalue"]),"0.00",1)+"%")
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

    if eitem["y_salegain"]:
        ritem.setdefault('month_salegain_estimate',mtu.convertToStr(eitem['y_salegain']))
    else:
        ritem.setdefault('month_salegain_estimate',"0.0")

    if eitem["y_salegain"] > 0:
        ritem.setdefault('month_salegain_complet_progress',mtu.convertToStr(mtu.quantize(monthItem["m_salegain"])*decimal.Decimal("100.0")/mtu.quantize(eitem["y_salegain"]),"0.00",1)+"%")
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



@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass