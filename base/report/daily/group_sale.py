#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import Kshopsale,BasShopRegion,Estimate
from django.db import connection
from django.http import HttpResponse
import datetime,calendar,decimal
import xlwt3 as xlwt

@csrf_exempt
def index(request):
     date = DateUtil.get_day_of_day(-1)
     yesterday = date.strftime("%Y-%m-%d")

     #查询当月销售
     sql = "CALL k_d_wholesale ('{start}','{end}') ".format(start=yesterday,end=yesterday)
     cursor = connection.cursor()
     cursor.execute(sql)
     list = cursor.fetchall()
     rlist = []
     sumDict = {}
     for item in list:
        row = {}
        rlist.append(row)
        row.setdefault("sdate",item[0].strftime("%Y-%m-%d"))
        row.setdefault("shopid",item[1])
        row.setdefault("shopnm",item[2].strip())
        if item[3]:
            row.setdefault("tradeprice",float(item[3]))   #平均客单
        else:
            row.setdefault("tradeprice",0.00)
        if item[4]:
            row.setdefault("tradenumber",int(item[4]))  #总客流
        else:
            row.setdefault("tradenumber",0)
        if item[5]:
            row.setdefault("salevalue",float(item[5]))   #销售金额
        else:
            row.setdefault("salevalue",0.00)
        if item[6]:
            row.setdefault("discvalue",float(item[6]))   #折扣金额
        else:
            row.setdefault("discvalue",0.00)
        if item[7]:
            row.setdefault("sale",float(item[7]))    #实际销售
        else:
            row.setdefault("sale",0.00)
        if item[8]:
            row.setdefault("costvalue",float(item[8]))  #销售成本
        else:
            row.setdefault("costvalue",0.00)
        if item[9]:
            row.setdefault("salegain",float(item[9]))   #毛利
        else:
            row.setdefault("salegain",0.00)
        if item[10]:
            row.setdefault("gaintx",float(item[10]))   #毛利率
        else:
            row.setdefault("gaintx",0.00)
        if item[11]:
            row.setdefault("wsalevalue",float(item[11]))  #批发实际销售
        else:
            row.setdefault("wsalevalue",0.00)
        if item[12]:
            row.setdefault("wcostvalue",float(item[12])) #批发销售成本
        else:
            row.setdefault("wcostvalue",0.00)
        if item[13]:
            row.setdefault("wsalegain",float(item[13])) #批发毛利
        else:
            row.setdefault("wsalegain",0.00)
        if item[14]:
            row.setdefault("wgaintx",float(item[14]))  #批发毛利率
        else:
            row.setdefault("wgaintx",0.00)

     #计算月累加合计
     qtype = mtu.getReqVal(request,"qtype","1")
     if qtype == "1":
         return render(request, "report/daily/group_sale.html",{"rlist":rlist,"sumDict":sumDict})
     else:
         return export(request,rlist,sumDict)

def export(request,rlist,sumList):

    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)

    #写入sheet1 月累计销售报表
   #writeDataToSheet1(wb,rlist,sumList)

    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d")+"group_daily_sale"

    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response