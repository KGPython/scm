# -*- coding:utf-8 -*-
__author__ = 'admin'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import xlwt3 as xlwt
from base.utils import MethodUtil as mtu,DateUtil
from django.http import HttpResponse
from base.models import KgNegStock
import decimal,datetime
def index(request):
    sgroupid = request.REQUEST.get('sgroupid')
    title = ''
    if sgroupid == '2':
        title = '食品'
    if sgroupid == '3':
        title = '非食'
    yesterday = DateUtil.get_day_of_day(-1)
    kwargs = {}
    kwargs.setdefault('saledate',yesterday)
    kwargs.setdefault('sgroupid',sgroupid)
    resList = KgNegStock.objects.values('shopid','shopname','sgroupid','sgroupname','goodsid','goodsname','qty','costvalue','spec','unitname','deptid','deptname','venderid','vendername','promflag','openqty','receiptdate','onreceiptqty','saledate')\
        .filter(**kwargs).order_by('shopid')
    formate_data(resList)
    qtype = mtu.getReqVal(request,"qtype","1")
    if qtype == "1":
        return render(request,'report/abnormal/negStock.html',locals())
    else:
        return export(resList,yesterday,title)

def formate_data(rlist):
    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item,decimal.Decimal):
                rows[k] = "%0.2f" % float(item)
            if isinstance(item,datetime.datetime):
                rows[k] = item.strftime("%Y-%m-%d")
            if not item:
                rows[k] = ''

def export(resList,yesterday,title):
    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)
    writeDataToSheet2(wb,resList,title)

    outtype = 'application/vnd.ms-excel;'
    fname = yesterday.strftime('%m.%d')+"_abnormal_negStock"
    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response

def writeDataToSheet2(wb,resList,title):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month

    sheet2 = wb.add_sheet("%s负库存商品报告"%title,cell_overwrite_ok=True)
    titlesSheet2 = [
        [("（%s月）%s负库存商品报告"%(month,title),0,1,7)],
        [("报表日期",3,1,1),("%s年-%s月-%s日"%(year,month,date.day),4,1,3)],
        [
            ("门店编号",0,1,1),("门店名称",1,1,1),("管理类别码",2,1,1),("管理类别名称",3,1,1),("小类编码",4,1,1),
            ("小类名称",5,1,1),("商品编码",6,1,1),("商品名称",7,1,1),("商品规格",8,1,1),("销售单位",9,1,1),
            ("负库存数量",10,1,1),("负库存金额",11,1,1),("解释原因",12,1,1),("解决方案",13,1,1),("解决时间",14,1,1)
        ]
    ]
    keylistSheet2 = ['shopid','shopname','sgroupid','sgroupname','deptid','deptname','goodsid','goodsname','spec','unitname'
                     ,'qty','costvalue','reason1','reason2','reason3'
                     ]
    widthList = [600,1100,600,600,600,800,600,1100,600,600,600,600,2000,2000,2000]

    mtu.insertTitle2(sheet2,titlesSheet2,keylistSheet2,widthList)
    mtu.insertCell2(sheet2,3,resList,keylistSheet2,None)