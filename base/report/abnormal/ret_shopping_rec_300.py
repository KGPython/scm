# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil, MethodUtil as mtu
from base.models import Kglistnoret, BasPurLog
from django.http import HttpResponse
import datetime, calendar, decimal
import xlwt3 as xlwt


@csrf_exempt
def index(request):
    yesterday = DateUtil.get_day_of_day(-1)

    rlist = Kglistnoret.objects.values("shopid", "sdate", "stime", "listno", "posid", "cashierid", "name", "payreson",
                                       "paytype", "payvalue", "cardno").filter(sdate=yesterday)

    formate_data(rlist)

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
        return render(request, "report/abnormal/negprofit_lte200.html", {"rlist": list(rlist)})
    else:
        return export(rlist, yesterday)


def export(rlist, yesterday):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1 门店
    writeDataToSheet1(wb, rlist)

    outtype = 'application/vnd.ms-excel;'
    fname = yesterday.strftime("%m.%d") + "negprofit_lte200"

    response = mtu.getResponse(HttpResponse(), outtype, '%s.xls' % fname)
    wb.save(response)
    return response


def writeDataToSheet1(wb, rlist):
    sheet = wb.add_sheet("单张小票退货超300", cell_overwrite_ok=True)

    titles = [[("负毛利大于200", 0, 1, 15)],
              [("机构编码", 0, 1, 1), ("销售日期", 1, 1, 1), ("时间", 2, 1, 1), ("小票单号", 3, 1, 1), ("pos机号", 4, 1, 1),
               ("收银员号", 5, 1, 1), ("收银员名", 6, 1, 1), ("支付原因", 7, 1, 1), ("支付类型", 8, 1, 1), ("支付金额", 9, 1, 1)],
              ]

    keylist = ['shopid', 'sdate', 'stime', 'listno', 'posid', 'cashierid', 'name', 'payreson', 'paytype',
               'payvalue', 'cardno']
    widthlist = [800, 1000, 800, 800, 2000, 800, 800, 800, 800, 800, 800]

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
