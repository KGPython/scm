# -*- coding:utf-8 -*-
__author__ = 'end-e'

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil, MethodUtil as mtu
from base.models import BasPurLog
import datetime, calendar, decimal
import xlwt3 as xlwt


@csrf_exempt
def index(request):
    yearandmon = DateUtil.getyearandmonth()
    # 当前月份第一天
    monfirstday = DateUtil.get_firstday_of_month(yearandmon[0], yearandmon[1])
    # 当前月份最后一天
    monlastday = DateUtil.get_lastday_month()
    # 今天
    today = DateUtil.todaystr()
    # 昨天
    yesterday = DateUtil.get_yesterday()
    # 获取门店信息
    getshopname = getshopid()

    conn = mtu.getMysqlConn()
    sqltop = "select shopid, sum(shopsale) as shopsalesum, sum(ret) as retsum, (sum(ret) / sum(shopsale)) as retrate " \
             "from `KGshopretsale` " \
             "where sdate between '" + monfirstday + "' and '" + yesterday + "' " \
                                                                             "group by shopid " \
                                                                             "order by shopid"

    cur = conn.cursor()
    cur.execute(sqltop)
    listtop = cur.fetchall()
    # 最后一行的合计
    listtopTotal = {'sequenceNumber': '合计', 'shopid': '', 'shopname': '', 'shopsalesum': '', 'retsum': '', 'retrate': ''}
    # 汇总总计（每月1日到当日）
    tempshopsalesum = 0.00
    tempretsum = 0.00

    # 格式化数据
    paiming = 1
    for i in range(0, len(listtop)):
        for key in listtop[i].keys():
            row = listtop[i][key]
            if row == None:
                listtop[i][key] = ''
            else:
                if isinstance(row, decimal.Decimal) and key == 'retrate':
                    listtop[i][key] = str(abs(float("%0.2f" % float(listtop[i][key] * 100)))) + '%'
                elif isinstance(row, decimal.Decimal) and key == 'retsum':
                    listtop[i][key] = abs(float("%0.2f" % float(listtop[i][key])))
                elif isinstance(row, decimal.Decimal):
                    listtop[i][key] = "%0.2f" % float(listtop[i][key])
                else:
                    listtop[i][key] = listtop[i][key]

        # 添加汇总合计
        tempshopsalesum += float(listtop[i]['shopsalesum'])
        tempretsum += float(listtop[i]['retsum'])

        # 添加序号
        listtop[i]['sequenceNumber'] = paiming
        paiming += 1

        sql = "select sdate, shopid, shopsale, ret, ret / shopsale as retc " \
              "from `KGshopretsale` " \
              "where shopid='" + listtop[i]['shopid'] + "' " \
                                                        "and sdate between '" + monfirstday + "' and '" + yesterday + "'"

        cur = conn.cursor()
        cur.execute(sql)
        listdetail = cur.fetchall()

        for item in listdetail:
            date = str(item['sdate'])[8:10]

            if (not item['ret']):
                listtop[i]['retsum_' + date] = 0
            else:
                listtop[i]['retsum_' + date] = abs(float(item['ret']))
            if 'retsum_' + date in listtopTotal:
                listtopTotal['retsum_' + date] += listtop[i]['retsum_' + date]
            else:
                listtopTotal['retsum_' + date] = listtop[i]['retsum_' + date]

            if (not item['shopsale']):
                listtop[i]['shopsalesum_' + date] = 0
            else:
                listtop[i]['shopsalesum_' + date] = float(item['shopsale'])
            if 'shopsalesum_' + date in listtopTotal:
                listtopTotal['shopsalesum_' + date] += listtop[i]['shopsalesum_' + date]
            else:
                listtopTotal['shopsalesum_' + date] = listtop[i]['shopsalesum_' + date]

            if (not item['retc']):
                listtop[i]['retrate_' + date] = 0
            else:
                listtop[i]['retrate_' + date] = str(abs(float("%0.2f" % (item['retc'] * 100)))) + '%'

            # 添加当日汇总
            listtopTotal['retsum_' + date] = float("%0.2f" % (listtopTotal['retsum_' + date]))
            listtopTotal['shopsalesum_' + date] = float("%0.2f" % (listtopTotal['shopsalesum_' + date]))
            listtopTotal['retrate_' + date] = str(float("%0.2f" % (listtopTotal['retsum_' + date] / listtopTotal['shopsalesum_' + date] * 100))) + '%'

    # 添加门店名称
    for i in range(0, len(listtop)):
        for j in range(0, len(getshopname)):
            if listtop[i]['shopid'] == getshopname[j]['ShopID']:
                listtop[i]['shopname'] = getshopname[j]['ShopName'].strip()

    # 合计转换数据格式
    listtopTotal['shopsalesum'] = float("%0.2f" % tempshopsalesum)
    listtopTotal['retsum'] = float("%0.2f" % tempretsum)
    listtopTotal['retrate'] = str("%0.2f" % float(float(listtopTotal['retsum'] / listtopTotal['shopsalesum']) * 100)) + '%'

    # 转换为dict，导出excel
    TotalDict = {'listtopTotal':listtopTotal}


    # 退货明细
    sqldetail = "select shopid, shopname, sdate, stime, listno, posid, cashierid, goodsid, goodsname, deptid, amount, sale " \
                "from `KGshopretsaleitem` " \
                "where sdate='" + yesterday + "' order by shopid"
    cur = conn.cursor()
    cur.execute(sqldetail)
    retdetail = cur.fetchall()
    # 格式化数据
    for i in range(0, len(retdetail)):
        for key in retdetail[i].keys():
            row = retdetail[i][key]
            if row == None:
                listtop[i][key] = ''
            else:
                if isinstance(row, decimal.Decimal):
                    retdetail[i][key] = "%0.2f" % float(retdetail[i][key])
                elif isinstance(row, datetime.datetime):
                    retdetail[i][key] = retdetail[i][key].strftime("%Y-%m-%d")
                else:
                    retdetail[i][key] = retdetail[i][key]

    mtu.close(conn, cur)

    exceltype = mtu.getReqVal(request, "exceltype", "2")
    # 操作日志
    if exceltype=='2':
        qtype = "1"
    else:
        qtype = "2"
    key_state = mtu.getReqVal(request, "key_state", '')
    if exceltype == '1' and (not key_state or key_state != '2'):
        exceltype = '2'

    path = request.path
    today = datetime.datetime.today();
    ucode = request.session.get("s_ucode")
    uname = request.session.get("s_uname")
    BasPurLog.objects.create(name="顾客退货率", url=path, qtype=qtype, ucode=ucode,uname=uname, createtime=today)

    if exceltype == '1':
        return export(request, listtop, TotalDict, retdetail)
    else:
        return render(request, "report/daily/customer_returns.html", locals())


def getshopid():
    '''
    获取门店编码
    :return list:
    '''
    conn = mtu.getMysqlConn()
    cur = conn.cursor()
    sql = "select ShopID, ShopName from bas_shop_region"
    cur.execute(sql)
    res = cur.fetchall()
    # 释放
    mtu.close(conn, cur)
    return res


def export(request, listtop, TotalDict, retdetail):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1
    writeDataToSheet1(wb, listtop, TotalDict)
    # 写入sheet2
    writeDataToSheet2(wb, retdetail)

    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d") + "customer_returns"
    response = mtu.getResponse(HttpResponse(), outtype, '%s.xls' % fname)
    wb.save(response)
    return response


def writeDataToSheet1(wb, listtop, TotalDict):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet1 = wb.add_sheet("门店顾客退货率", cell_overwrite_ok=True)

    titles = [
        [("（%s月）门店顾客退货率" % month, 0, 1, 13)],
        [("序号", 0, 2, 1), ("门店编码", 1, 2, 1), ("门店名称", 2, 2, 1), ('月累计退货', 3, 1, 3)],
        [('销售金额', 3, 1, 1), ('退货金额', 4, 1, 1), ('退货率', 5, 1, 1)]
    ]

    keylist = ['sequenceNumber', 'shopid', 'shopname', 'shopsalesum', 'retsum', 'retrate']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    trow1 = titles[1]
    trow2 = titles[2]

    n = 6
    for d in range(1, lastDay + 1):
        trow1.append((str(month) + '月' + str(d) + '日', n, 1, 3))
        trow2.append(('销售金额', n, 1, 1))
        trow2.append(('退货金额', n + 1, 1, 1))
        trow2.append(('退货率', n + 2, 1, 1))
        widthList.append(600)
        widthList.append(400)
        widthList.append(400)
        n += 3
        if d < 10:
            keylist.append('retsum_0' + str(d))
            keylist.append('shopsalesum_0' + str(d))
            keylist.append('retrate_0' + str(d))
        else:
            keylist.append('retsum_' + str(d))
            keylist.append('shopsalesum_' + str(d))
            keylist.append('retrate_' + str(d))


    # 日销售报表
    mtu.insertTitle2(sheet1, titles, keylist, widthList)
    mtu.insertCell2(sheet1, 3, listtop, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(listtop)
    mtu.insertSum2(sheet1, keylist, titlesLen + listTopLen, TotalDict, 3)


def writeDataToSheet2(wb, retdetail):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet2 = wb.add_sheet("退货明细", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）门店顾客退货明细" % (month, date.day), 0, 1, 12)],
        [("门店编码", 0, 2, 1), ("门店名称", 1, 2, 1), ("销售日期", 2, 2, 1), ("销售时间", 3, 2, 1), ("退货小票", 4, 2, 1),
         ("posid", 5, 2, 1), ("收银员工号", 6, 2, 1), ("商品编码", 7, 2, 1), ("商品名称", 8, 2, 1), ("类别编码", 9, 2, 1),
         ("退货数量", 10, 2, 1), ("退货金额", 11, 2, 1)],
    ]

    keylist = ['shopid', 'shopname', 'sdate', 'stime', 'listno', 'posid', 'cashierid', 'goodsid', 'goodsname', 'deptid', 'amount',
               'sale']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet2, titles, keylist, widthList)
    mtu.insertCell2(sheet2, 3, retdetail, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(retdetail)


def ranking(lis,key,name):
    lis.sort(key=lambda x:x[key])
    j = 1
    for i in range(0,len(lis)):
        if i > 0:
            a = lis[i-1]
            b = lis[i]
            if float(a[key]) != float(b[key]):
                j += 1
            b[name]= j
            a[key] = str(a[key])+'%'
        else:
            a = lis[i]
            a[name]= j
    return lis
