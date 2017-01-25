#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import Kgprofit,BasPurLog
from django.http import HttpResponse
import datetime,calendar,decimal,json
import xlwt3 as xlwt
from django.views.decorators.cache import cache_page

def query(date):
    karrs = {}
    karrs.setdefault("bbdate", "{start}".format(start=date))
    rlist = Kgprofit.objects.values("bbdate", "sdate", "shopid", "shopname", "goodsid", "goodsname", "deptid",
                                    "deptname", "qty", "profit", "stockqty", "truevalue", "costvalue") \
        .filter(**karrs).exclude(shopid='C009').order_by("bbdate", "shopid", "goodsid", "sdate")
    formate_data(rlist)
    return rlist


@cache_page(60 * 2 ,key_prefix='abnormal_negprofit_past_3days')
@csrf_exempt
def index(request):
     yesterday = DateUtil.get_day_of_day(-1)
     qtype = mtu.getReqVal(request,"qtype","1")

     #操作日志
     if not qtype:
         qtype = "1"
     path = request.path
     today = datetime.datetime.today()
     ucode = request.session.get("s_ucode")
     uname = request.session.get("s_uname")
     BasPurLog.objects.create(name="商品连续3天负毛利",url=path,qtype=qtype,ucode=ucode,uname=uname,createtime=today)

     if qtype == "1":
         data = query(yesterday)
         return render(request, "report/abnormal/negprofit_past3days.html", {"rlist":list(data)})
     else:
         fname = yesterday.strftime("%m.%d") + "_abnormal_negprofit_past3day.xls"
         return export(fname,yesterday)

import base.report.Excel as excel
def export(fname,yesterday):
    if not excel.isExist(fname):
        data = query(yesterday)
        creatExcel(fname,data)
    res = {}
    res['fname'] = fname
    return HttpResponse(json.dumps(res))

def creatExcel(fname,data):
    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)
    writeDataToSheet1(wb,data)
    excel.saveToExcel(fname,wb)

def writeDataToSheet1(wb,rlist):
    sheet = wb.add_sheet("连续三天负毛利明细",cell_overwrite_ok=True)

    titles = [[("连续三天负毛利明细" ,0,1,15)],
              [("机构编码",0,1,1),("机构名称",1,1,1),("销售日期",2,1,1),("商品编码",3,1,1),("商品名称",4,1,1),
               ("管理类别编码",5,1,1),("管理类别名称",6,1,1),("销售金额",7,1,1),("销售数量",8,1,1),("成本金额",9,1,1),
               ("亏损金额",10,1,1),("库存数量",11,1,1),("解释原因",12,1,1),("解决方案",13,1,1),("解决时间",14,1,1)],
              ]

    keylist = ['shopid','shopname','sdate','goodsid','goodsname','deptid','deptname','truevalue','qty',
               'costvalue','profit','stockqty','solvereason','solvesolution','solvetime']
    widthlist = [800,1000,800,800,2000,800,800,800,800,800,800,800,800,800,800]

    mtu.insertTitle2(sheet,titles,keylist,widthlist)
    mtu.insertCell2(sheet,2,rlist,keylist,None)

def formate_data(rlist):
    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item,decimal.Decimal):
                rows[k] = "%0.2f" % float(item)
            if isinstance(item,datetime.datetime):
                rows[k] = item.strftime("%Y-%m-%d")

