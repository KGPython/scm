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
    sqltop = "select shopid, sum(costvalue) as costvaluesum, sum(reth) as rethsum, (sum(reth) / sum(costvalue)) as retrate " \
             "from `KGretshop` " \
             "where sdate between '" + monfirstday + "' and '" + yesterday + "' " \
                                                                             "group by shopid " \
                                                                             "order by shopid"

    cur = conn.cursor()
    cur.execute(sqltop)
    listtop = cur.fetchall()
    # 最后一行的合计
    listtopTotal = {'sequenceNumber': '合计', 'shopid': '', 'shopname': '', 'costvaluesum': '', 'rethsum': '',
                    'retrate': ''}
    # 汇总总计（每月1日到当日）
    tempcostvaluesum = 0.00
    temprethsum = 0.00

    # 格式化数据
    paiming = 1
    for i in range(0, len(listtop)):
        for key in listtop[i].keys():
            row = listtop[i][key]
            if row == None:
                listtop[i][key] = ''
            else:
                if isinstance(row, decimal.Decimal) and key == 'retrate':
                    listtop[i][key] = str(float("%0.2f" % float(listtop[i][key] * 100))) + '%'
                elif isinstance(row, decimal.Decimal):
                    listtop[i][key] = "%0.2f" % float(listtop[i][key])
                else:
                    listtop[i][key] = listtop[i][key]

        # 添加序号
        listtop[i]['sequenceNumber'] = paiming
        paiming += 1

        # 添加汇总合计
        tempcostvaluesum += float(listtop[i]['costvaluesum'])
        temprethsum += float(listtop[i]['rethsum'])

        sql = "select sdate, shopid, costvalue, reth, reth / costvalue as ret " \
              "from `KGretshop` " \
              "where shopid='" + listtop[i]['shopid'] + "' " \
                                                        "and sdate between '" + monfirstday + "' and '" + yesterday + "'"
        cur = conn.cursor()
        cur.execute(sql)
        listdetail = cur.fetchall()

        for item in listdetail:
            date = str(item['sdate'])[8:10]

            if (not item['reth']):
                listtop[i]['rethsum_' + date] = 0
            else:
                listtop[i]['rethsum_' + date] = float(item['reth'])
            if 'rethsum_' + date in listtopTotal:
                listtopTotal['rethsum_' + date] += listtop[i]['rethsum_' + date]
            else:
                listtopTotal['rethsum_' + date] = listtop[i]['rethsum_' + date]

            if (not item['costvalue']):
                listtop[i]['costvaluesum_' + date] = 0
            else:
                listtop[i]['costvaluesum_' + date] = float(item['costvalue'])
            if 'costvaluesum_' + date in listtopTotal:
                listtopTotal['costvaluesum_' + date] += listtop[i]['costvaluesum_' + date]
            else:
                listtopTotal['costvaluesum_' + date] = listtop[i]['costvaluesum_' + date]

            if (not item['ret']):
                listtop[i]['retrate_' + date] = 0
            else:
                listtop[i]['retrate_' + date] = str(float("%0.2f" % (item['ret'] * 100))) + '%'

            # 添加当日汇总
            listtopTotal['rethsum_' + date] = float("%0.2f" % (listtopTotal['rethsum_' + date]))
            listtopTotal['costvaluesum_' + date] = float("%0.2f" % (listtopTotal['costvaluesum_' + date]))
            listtopTotal['retrate_' + date] = str(float("%0.2f" % (listtopTotal['rethsum_' + date] / listtopTotal['costvaluesum_' + date] * 100))) + '%'

    # 添加门店名称
    for i in range(0, len(listtop)):
        for j in range(0, len(getshopname)):
            if listtop[i]['shopid'] == getshopname[j]['ShopID']:
                listtop[i]['shopname'] = getshopname[j]['ShopName'].strip()

    # 合计转换数据格式
    listtopTotal['costvaluesum'] = "%0.2f" % tempcostvaluesum
    listtopTotal['rethsum'] = "%0.2f" % temprethsum
    tempcandr = "%0.2f" % (temprethsum / tempcostvaluesum)
    listtopTotal['retrate'] = str("%0.2f" % float(float(tempcandr) * 100)) + '%'

    mtu.close(conn, cur)

    # 转换为dict，导出excel
    TotalDict = {'listtopTotal':listtopTotal}
    exceltype = mtu.getReqVal(request, "exceltype", "2")
    # 操作日志
    if exceltype=="2":
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
    BasPurLog.objects.create(name="供应商退货率", url=path, qtype=qtype, ucode=ucode,uname=uname, createtime=today)

    if exceltype == '1':
        return export(request, listtop, TotalDict)
    else:
        return render(request, "report/daily/supplier_returns.html", locals())


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


def export(request, listtop, TotalDict):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1
    writeDataToSheet1(wb, listtop, TotalDict)

    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d") + "supplier_returns"
    response = mtu.getResponse(HttpResponse(), outtype, '%s.xls' % fname)
    wb.save(response)
    return response


def writeDataToSheet1(wb, listtop, TotalDict):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet1 = wb.add_sheet("门店供应商退货率", cell_overwrite_ok=True)

    titles = [
        [("（%s月）门店供应商退货率" % month, 0, 1, 13)],
        [("序号", 0, 2, 1), ("门店编码", 1, 2, 1), ("门店名称", 2, 2, 1), ('月累计退货', 3, 1, 3)],
        [('销售成本', 3, 1, 1), ('退货金额', 4, 1, 1), ('退货率', 5, 1, 1)]
    ]

    keylist = ['sequenceNumber', 'shopid', 'shopname', 'costvaluesum', 'rethsum', 'retrate']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    trow1 = titles[1]
    trow2 = titles[2]

    n = 6
    for d in range(1, lastDay + 1):
        trow1.append((str(month) + '月' + str(d) + '日', n, 1, 3))
        trow2.append(('销售成本', n, 1, 1))
        trow2.append(('退货金额', n + 1, 1, 1))
        trow2.append(('退货率', n + 2, 1, 1))
        widthList.append(600)
        widthList.append(400)
        widthList.append(400)
        n += 3
        if d < 10:
            keylist.append('costvaluesum_0' + str(d))
            keylist.append('rethsum_0' + str(d))
            keylist.append('retrate_0' + str(d))
        else:
            keylist.append('costvaluesum_' + str(d))
            keylist.append('rethsum_' + str(d))
            keylist.append('retrate_' + str(d))

    # 日销售报表
    mtu.insertTitle2(sheet1, titles, keylist, widthList)
    mtu.insertCell2(sheet1, 3, listtop, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(listtop)
    mtu.insertSum2(sheet1, keylist, titlesLen + listTopLen, TotalDict, 3)
