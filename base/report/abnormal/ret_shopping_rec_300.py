# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil, MethodUtil as mtu
from base.models import Kglistnoret, Kggoodsret, BasPurLog
from django.http import HttpResponse
import datetime, decimal,json
import xlwt3 as xlwt
from django.views.decorators.cache import cache_page
from base.report.common import Method as reportMth

def query(date):
    rbacDepartList, rbacDepart = reportMth.getRbacDepart(11)
    rbacClassList, rbacClass = reportMth.getRbacClass()

    rlist = Kglistnoret.objects\
            .values("shopid", "sdate", "stime", "listno", "posid", "cashierid",
                    "name", "payreson","paytype", "payvalue")\
            .filter(sdate=date,shopid__in=rbacDepartList)

    formate_data(rlist)

    # 商品退货明细
    conn= mtu.getMysqlConn()
    sql = "SELECT shopid, sdate, stime, listno, posid, cashierid, name, DeptID, DeptName, goodsid, goodsname, xAmount," \
          "salevalue, DiscValue, truevalue, SaleType, Price, DiscType " \
          "FROM `kggoodsret` " \
          "WHERE (`shopid` IN ({rbacDepart}) AND `sdate` = '{date}' " \
          "AND LEFT(`DeptID`,2) IN ({rbacClass}))"\
          .format(rbacDepart=rbacDepart,date=date,rbacClass=rbacClass)
    cur = conn.cursor()
    cur.execute(sql)
    dlist = cur.fetchall()
    cur.close()
    conn.close()
    formate_data(dlist)
    data = {"rlist": list(rlist), 'dlist': list(dlist)}
    return data


# @cache_page(60*2 ,key_prefix='abnormal_ret_shopping_rec_300')
@csrf_exempt
def index(request):
    yesterday = DateUtil.get_day_of_day(-1)

    qtype = mtu.getReqVal(request, "qtype", "1")
    # 操作日志
    if not qtype:
        qtype = "1"
    path = request.path
    today = datetime.datetime.today()
    ucode = request.session.get("s_ucode")
    uname = request.session.get("s_uname")
    BasPurLog.objects.create(name="单张小票退货超300", url=path, qtype=qtype, ucode=ucode, uname=uname, createtime=today)

    if qtype == "1":
        data = query(yesterday)
        return render(request, "report/abnormal/ret_shopping_rec_300.html",data)
    else:
        fname = yesterday.strftime("%m.%d") + "_abnormal_ret_shopping_rec_300.xls"
        return export(fname,yesterday)

import base.report.Excel as excel
def export(fname,yesterday):
    if not excel.isExist(fname):
        data = query(yesterday)
        createExcel(fname,data)
    res = {}
    res['fname'] = fname
    return HttpResponse(json.dumps(res))

def createExcel(fname,data):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1
    writeDataToSheet1(wb, data['rlist'])
    # 写入sheet2
    writeDataToSheet2(wb, data['dlist'])
    excel.saveToExcel(fname,wb)


def writeDataToSheet1(wb, rlist):
    sheet = wb.add_sheet("单张小票退货超300", cell_overwrite_ok=True)

    titles = [[("单张小票退货超300", 0, 1, 10)],
              [("门店编码", 0, 1, 1), ("销售日期", 1, 1, 1), ("时间", 2, 1, 1), ("小票单号", 3, 1, 1), ("pos机号", 4, 1, 1),
               ("收银员号", 5, 1, 1), ("收银员名", 6, 1, 1), ("支付原因", 7, 1, 1), ("支付类型", 8, 1, 1), ("支付金额", 9, 1, 1)],
              ]

    keylist = ['shopid', 'sdate', 'stime', 'listno', 'posid', 'cashierid', 'name', 'payreson', 'paytype', 'payvalue']
    widthlist = [800, 800, 800, 800, 800, 800, 800, 800, 800, 800]

    mtu.insertTitle2(sheet, titles, keylist, widthlist)
    mtu.insertCell2(sheet, 2, rlist, keylist, None)


def writeDataToSheet2(wb, rlist):
    sheet = wb.add_sheet("商品退货明细", cell_overwrite_ok=True)

    titles = [[("商品退货明细", 0, 1, 16)],
              [("门店编码", 0, 1, 1), ("销售日期", 1, 1, 1), ("时间", 2, 1, 1), ("小票单号", 3, 1, 1), ("pos机号", 4, 1, 1),
               ("收银员号", 5, 1, 1), ("收银员名", 6, 1, 1), ("商品名称", 7, 1, 1), ("商品编码", 8, 1, 1),
               ("销售数量", 9, 1, 1), ("销售金额", 10, 1, 1), ("折扣金额", 11, 1, 1), ("实际销售", 12, 1, 1),
               ("销售类型", 13, 1, 1), ("售价", 14, 1, 1), ("解释原因", 15, 1, 1)],
              ]

    keylist = ['shopid', 'sdate', 'stime', 'listno', 'posid', 'cashierid', 'name', 'goodsname', 'deptid', 'xamount', \
               'salevalue', 'discvalue', 'truevalue', 'saletype', 'price']
    widthlist = [800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800]

    mtu.insertTitle2(sheet, titles, keylist, widthlist)
    mtu.insertCell2(sheet, 2, rlist, keylist, None)


def formate_data(rlist):
    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item, decimal.Decimal):
                rows[k] = "%0.2f" % float(item)
            if isinstance(item, datetime.datetime):
                rows[k] = item.strftime("%Y-%m-%d")
