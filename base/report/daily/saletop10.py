# -*- coding:utf-8 -*-
__author__ = 'end-e 20160602'

import calendar
import datetime
import decimal
import json

import xlwt3 as xlwt
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from base.models import BasPurLog
from base.report.common import Method as reportMth
from base.utils import DateUtil, MethodUtil as mtu
from base.report.common import Excel

def initDepartData(id,yesterday):
    rbacDepartList, rbacDepart = reportMth.getRbacDepart(11)

    # 连接数据库
    conn = mtu.getMysqlConn()

    # 获取部类编码
    classcode = getclasscode()
    # 获取所有商品的类别编码
    allcode = getallcode()
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

    subcate = subcate.get(id)
    sqlsubcate = ','.join(subcate)
    sql = "select shopid, goodsid, goodsname, SaleQty, SaleValue, SaleCost, gpvalue, gprate, qty, costvalue, cprice, price " \
            "from `kwsaletop10` " \
            "where deptid in ({sqlsubcate}) and sdate='{yesterday}' and shopid in ({rbacDepart}) " \
            "order by shopid, SaleValue desc" \
        .format(sqlsubcate=sqlsubcate, yesterday=str(yesterday), rbacDepart=rbacDepart)
    cur = conn.cursor()
    cur.execute(sql)
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
    # 将退货数据过滤，值为负
    rowsfilter = []
    for i in range(0, len(rows)):
        if float(rows[i]['SaleQty']) < 0:
            continue
        else:
            rowsfilter.append(rows[i])


    lis = []
    unit = []
    # 获取门店编码
    shopsid = getshopid()
    for sid in shopsid:
        i = 0
        for row in rows:
            if sid['ShopID'] == row['shopid'] and i < 10:
                row['shopid'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis.append(row)
                i += 1
            else:
                continue
        unit.append(i)

    return lis,unit


def query(yesterday):
    rbac = caches['redis2'].get('rbac_role')

    rbacDepart = rbac['depart']
    if len(rbacDepart):
        rbacDepart = json.loads(rbacDepart)
        rbacDepart = rbacDepart['sub'][0:len(rbacDepart['sub']) - 1]
        rbacDepartList = rbacDepart.split(',')
        rbacDepart = '"' + '","'.join(rbacDepartList) + '"'

    rbacClassList = []
    rbacClass = ''
    rbacCategory = rbac['category']
    if len(rbacCategory):
        rbacCategory = rbacCategory.replace('},', '}$')
        rbacCategoryList = rbacCategory.split('$')
        for category in rbacCategoryList:
            category = json.loads(category)
            ClassStr = category['sub'][0:len(category['sub']) - 1]
            ClassList = ClassStr.split(',')
            ClassStr = '"' + '","'.join(ClassList) + '"'

            rbacClassList += ClassList
            rbacClass += ClassStr + ','

    rbacClass = rbacClass[0:len(rbacClass) - 1]

    yearandmon = DateUtil.getyearandmonth()
    # 当前月份第一天
    monfirstday = DateUtil.get_firstday_of_month(yearandmon[0], yearandmon[1])
    # 当前月份最后一天
    monlastday = DateUtil.get_lastday_month()
    # 今天
    today = DateUtil.todaystr()

    for C in rbacClassList:
        if C == '10':
            lis10, unit10 = initDepartData('10',yesterday)
        elif C == '11':
            lis11, unit11 = initDepartData('11', yesterday)
        elif C == '12':
            lis12, unit12 = initDepartData('12', yesterday)
        elif C == '13':
            lis13, unit13 = initDepartData('13', yesterday)
        elif C == '14':
            lis14, unit14 = initDepartData('14', yesterday)
        elif C == '15':
            lis15, unit15 = initDepartData('15', yesterday)
        elif C == '16':
            lis16, unit16 = initDepartData('16', yesterday)
        elif C == '17':
            lis17, unit17 = initDepartData('17', yesterday)
        elif C == '2':
            lis2, unit2 = initDepartData('2', yesterday)
        elif C == '3':
            lis3, unit3 = initDepartData('3', yesterday)
        elif C == '4':
            lis4, unit4 = initDepartData('4', yesterday)

    return locals()

# @cache_page(60*60*4,key_prefix='daily_sale_top10')
@csrf_exempt
def index(request):
    exceltype = mtu.getReqVal(request, "exceltype", "2")
    if exceltype=='2':
        qtype = "1"
    else:
        qtype = "2"
    key_state = mtu.getReqVal(request, "key_state", '')
    if exceltype == '1' and (not key_state or key_state != '2'):
        exceltype = '2'

    # 操作日志
    path = request.path
    today = datetime.datetime.today()
    ucode = request.session.get("s_ucode")
    uname = request.session.get("s_uname")
    BasPurLog.objects.create(name="超市课组销售前十", url=path, qtype=qtype, ucode=ucode,uname=uname, createtime=today)

    yesterday = DateUtil.get_day_of_day(-1)
    if exceltype == '1':
        fname = yesterday.strftime("%m.%d") + "_daily_saletop10_operate.xls"
        return export(fname,yesterday)
    else:
        data = query(yesterday)
        return render(request, "report/daily/saletop10.html", data)


def getshopid():
    '''
    获取门店编码
    :return list:
    '''
    conn = mtu.getMysqlConn()
    cur = conn.cursor()
    sql = "select ShopID, ShopName from bas_shop_region where ShopType=11"
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
    sql = "select distinct(deptid) from kwsaletop10"
    cur.execute(sql)
    res = cur.fetchall()
    # 释放
    cur.close()
    lis = []

    for y in res:
        lis.append(y['deptid'])

    return lis


def export(fname,yesterday):
    if not Excel.isExist(fname):
        data = query(yesterday)
        createExcel(fname, data)
    res = {}
    res['fname'] = fname
    return HttpResponse(json.dumps(res))


def createExcel(fname, data):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1
    writeDataToSheet1(wb, data['lis10'])
    # 写入sheet2
    writeDataToSheet2(wb, data['lis11'])
    # 写入sheet3
    writeDataToSheet3(wb, data['lis12'])
    # 写入sheet4
    writeDataToSheet4(wb, data['lis13'])
    # 写入sheet5
    writeDataToSheet5(wb, data['lis14'])
    # 写入sheet6
    writeDataToSheet6(wb, data['lis15'])
    # 写入sheet7
    writeDataToSheet7(wb, data['lis16'])
    # 写入sheet8
    writeDataToSheet8(wb, data['lis17'])
    # 写入sheet9
    writeDataToSheet9(wb, data['lis2'])
    # 写入sheet10
    writeDataToSheet10(wb, data['lis3'])
    # 写入sheet11
    writeDataToSheet11(wb, data['lis4'])

    Excel.saveToExcel(fname, wb)


def writeDataToSheet1(wb, lis10):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet10 = wb.add_sheet("10熟食", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（熟食）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet10, titles, keylist, widthList)
    mtu.insertCell2(sheet10, 3, lis10, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis10)


def writeDataToSheet2(wb, lis11):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet11 = wb.add_sheet("11水产", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（水产）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet11, titles, keylist, widthList)
    mtu.insertCell2(sheet11, 3, lis11, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis11)


def writeDataToSheet3(wb, lis12):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet12 = wb.add_sheet("12蔬菜", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（蔬菜）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet12, titles, keylist, widthList)
    mtu.insertCell2(sheet12, 3, lis12, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis12)


def writeDataToSheet4(wb, lis13):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet13 = wb.add_sheet("13烘烤", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（烘烤）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet13, titles, keylist, widthList)
    mtu.insertCell2(sheet13, 3, lis13, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis13)


def writeDataToSheet5(wb, lis14):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet14 = wb.add_sheet("14鲜肉", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（鲜肉）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet14, titles, keylist, widthList)
    mtu.insertCell2(sheet14, 3, lis14, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis14)


def writeDataToSheet6(wb, lis15):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet15 = wb.add_sheet("15干果干货", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（干果干货）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet15, titles, keylist, widthList)
    mtu.insertCell2(sheet15, 3, lis15, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis15)


def writeDataToSheet7(wb, lis16):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet16 = wb.add_sheet("16主食厨房", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（主食厨房）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet16, titles, keylist, widthList)
    mtu.insertCell2(sheet16, 3, lis16, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis16)


def writeDataToSheet8(wb, lis17):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet17 = wb.add_sheet("17水果", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（水果）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet17, titles, keylist, widthList)
    mtu.insertCell2(sheet17, 3, lis17, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis17)

def writeDataToSheet9(wb, lis2):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet2 = wb.add_sheet("2食品", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（食品）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet2, titles, keylist, widthList)
    mtu.insertCell2(sheet2, 3, lis2, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis2)


def writeDataToSheet10(wb, lis3):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet3 = wb.add_sheet("3用品", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（用品）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet3, titles, keylist, widthList)
    mtu.insertCell2(sheet3, 3, lis3, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis3)


def writeDataToSheet11(wb, lis4):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year, month)[1]

    sheet4 = wb.add_sheet("4家电", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（家电）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopid', 'paiming', 'goodsid', 'goodsname', 'SaleQty', 'SaleValue', 'SaleCost', 'gpvalue', 'gprate', \
               'qty', 'costvalue', 'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet4, titles, keylist, widthList)
    mtu.insertCell2(sheet4, 3, lis4, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis4)