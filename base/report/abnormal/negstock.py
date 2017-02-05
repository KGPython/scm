# -*- coding:utf-8 -*-
__author__ = 'admin'

import datetime
import decimal
import json

import xlwt3 as xlwt
from django.http import HttpResponse
from django.shortcuts import render

from base.models import BasPurLog
from base.report.common import Method as reportMth
from base.utils import MethodUtil as mtu,DateUtil


def query(sgroupid,date):
    rbacDepartList, rbacDepart = reportMth.getRbacDepart(11)
    rbacClassList, rbacClass = reportMth.getRbacClass()

    title = ''
    if sgroupid == '2':
        title = '食品'
    if sgroupid == '3':
        title = '非食'

    conn = mtu.getMysqlConn()
    sql= "SELECT `KGnegstock`.`shopid`, `KGnegstock`.`shopname`, `KGnegstock`.`sGroupID`, `KGnegstock`.`sGroupName`, " \
         "`KGnegstock`.`GoodsID`, `KGnegstock`.`GoodsName`, `KGnegstock`.`qty`, `KGnegstock`.`CostValue`, `KGnegstock`." \
         "`Spec`, `KGnegstock`.`UnitName`, `KGnegstock`.`deptid`, `KGnegstock`.`deptname`, `KGnegstock`.`Venderid`, " \
         "`KGnegstock`.`VenderName`, `KGnegstock`.`Promflag`, `KGnegstock`.`OpenQty`, `KGnegstock`.`ReceiptDate`, " \
         "`KGnegstock`.`OnReceiptQty`, `KGnegstock`.`SaleDate` " \
         "FROM `KGnegstock` " \
         "WHERE (`KGnegstock`.`shopid` IN ({rbacDepart}) AND `KGnegstock`.`SaleDate` = '{date}' " \
         "AND LEFT(`KGnegstock`.`deptid`,2) IN ({rbacClass}) AND `KGnegstock`.`sGroupID` = {sgroupid}) " \
         "ORDER BY `KGnegstock`.`shopid` ASC"\
        .format(rbacDepart=rbacDepart,rbacClass=rbacClass,date=date,sgroupid=sgroupid)
    cur = conn.cursor()
    cur.execute(sql)
    resList = cur.fetchall()
    cur.close()
    conn.close()
    formate_data(resList)

    return  locals()

# @cache_page(60 * 2 ,key_prefix='abnormal_negstock')
def index(request):
    sgroupid = request.REQUEST.get('sgroupid')
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
        data = query(sgroupid,yesterday)
        return render(request,'report/abnormal/negStock.html',data)
    else:
        fname = yesterday.strftime('%m.%d') + "_abnormal_negStock.xls"
        return export(fname,sgroupid,yesterday)

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


def export(fname,sgroupid,yesterday):
    if not Excel.isExist(fname):
        data = query(sgroupid,yesterday)
        createExcel(fname, data)
    res = {}
    res['fname'] = fname
    return HttpResponse(json.dumps(res))

def createExcel(fname, data):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    writeDataToSheet2(wb,data['resList'],data['title'])
    Excel.saveToExcel(fname, wb)

def writeDataToSheet2(wb,resList,title):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month

    sheet2 = wb.add_sheet("%s负库存商品报告"%title,cell_overwrite_ok=True)
    titlesSheet2 = [
        [("（%s月）%s负库存商品报告"%(month,title),0,1,15)],
        [("报表日期",11,1,1),("%s年-%s月-%s日"%(year,month,date.day),12,1,3)],
        [
            ("门店编号",0,1,1),("门店名称",1,1,1),("管理类别码",2,1,1),("管理类别名称",3,1,1),("小类编码",4,1,1),
            ("小类名称",5,1,1),("商品编码",6,1,1),("商品名称",7,1,1),("商品规格",8,1,1),("销售单位",9,1,1),
            ("负库存数量",10,1,1),("负库存金额",11,1,1),("解释原因",12,1,1),("解决方案",13,1,1),("解决时间",14,1,1)
        ]
    ]
    keylistSheet2 = ['shopid','shopname','sgroupid','sgroupname','deptid','deptname','goodsid','goodsname','spec','unitname'
                     ,'qty','costvalue','reason1','reason2','reason3'
                     ]
    widthList = [600,1400,600,600,600,800,600,1400,600,600,600,600,2000,2000,2000]

    mtu.insertTitle2(sheet2,titlesSheet2,keylistSheet2,widthList)
    mtu.insertCell2(sheet2,3,resList,keylistSheet2,None)