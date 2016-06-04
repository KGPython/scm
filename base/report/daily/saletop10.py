# -*- coding:utf-8 -*-
__author__ = 'end-e 20160602'

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime, calendar, decimal
from base.utils import DateUtil, MethodUtil as mtu
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
    yesterday = DateUtil.get_day_of_day(-1)

    # 获取部类编码
    classcode = getclasscode()

    # 获取所有商品的类别编码
    allcode = getallcode()

    # 获取门店编码
    shopsid = getshopid()

    # 查询某个部类下的子类编码
    subcate = {}
    # 将部类编码与子类编码组成dict
    for x in classcode:
        l = []
        for y in allcode:
            y = str(y)
            if len(x) == 1 and y[:1] == x:
                l.append(y)
            if len(x) == 2 and y[:2] == x:
                l.append(y)
        subcate.setdefault(x, l)

    subcate10 = subcate.get('10')
    sqlsubcate10 = ','.join(subcate10)

    sql = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, (svalue / num) as costprice, (svalue / num) as aveprice " \
          "from `kwsaletop` " \
          "where classsx in (" + sqlsubcate10 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, num desc"

    # 连接数据库
    conn = mtu.getMysqlConn()
    cur = conn.cursor()
    cur.execute(sql)
    # 获取10 部类下的销售数据
    rows = cur.fetchall()

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows)):
        for key in rows[i].keys():
            row = rows[i][key]
            if row is None:
                rows[i][key] = ''
            else:
                if isinstance(row, int):
                    rows[i][key] = str(rows[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows[i][key] = "%0.2f" % float(rows[i][key])
    # 10 熟食部类
    lis10 = []

    for sid in shopsid:
        print(sid)
        i = 0
        for row in rows:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip()
                row['paiming'] = i + 1
                lis10.append(row)
                i += 1
            else:
                continue

    # 关闭数据库
    mtu.close(conn, cur)
    exceltype = mtu.getReqVal(request, "exceltype", "2")
    if exceltype == '1':
        return export(request, lis10)
    else:
        return render(request, "report/daily/saletop10.html", locals())


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


def getclasscode():
    '''
    部类编码
    :return:
    '''
    parentcates = {
        '熟食部': '10',
        '水产': '11',
        '蔬菜': '12',
        '鲜肉': '14',
        '烘烤类': '13',
        '干果干货': '15',
        '主食厨房': '16',
        '水果': '17',
        '非食': '3',
        '商品部': '2',
        '家电部': '4'
    }

    # 获取部类编号
    lis = []

    for key, value in parentcates.items():
        lis.append(value)

    return lis


def getallcode():
    '''
    获取所有商品类别编码
    :return:
    '''
    conn = mtu.getMysqlConn()
    cur = conn.cursor()
    sql = "select distinct(classsx) from kwsaletop"
    cur.execute(sql)
    res = cur.fetchall()
    # 释放
    cur.close()
    lis = []

    for y in res:
        lis.append(y['classsx'])

    return lis


def export(request, lis10):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1
    writeDataToSheet1(wb, lis10)

    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d") + "saletop10_operate"
    response = mtu.getResponse(HttpResponse(), outtype, '%s.xls' % fname)
    wb.save(response)
    return response


def writeDataToSheet1(wb, lis10):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet = wb.add_sheet("（日）各店日销售排名", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'costprice', 'aveprice']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet, titles, keylist, widthList)
    mtu.insertCell2(sheet, 3, lis10, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis10)
