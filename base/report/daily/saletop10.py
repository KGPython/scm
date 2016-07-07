# -*- coding:utf-8 -*-
__author__ = 'end-e 20160602'

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
    subcate11 = subcate.get('11')
    subcate12 = subcate.get('12')
    subcate13 = subcate.get('13')
    subcate14 = subcate.get('14')
    subcate15 = subcate.get('15')
    subcate16 = subcate.get('16')
    subcate17 = subcate.get('17')
    subcate2 = subcate.get('2')
    subcate3 = subcate.get('3')
    subcate4 = subcate.get('4')
    sqlsubcate10 = ','.join(subcate10)
    sqlsubcate11 = ','.join(subcate11)
    sqlsubcate12 = ','.join(subcate12)
    sqlsubcate13 = ','.join(subcate13)
    sqlsubcate14 = ','.join(subcate14)
    sqlsubcate15 = ','.join(subcate15)
    sqlsubcate16 = ','.join(subcate16)
    sqlsubcate17 = ','.join(subcate17)
    sqlsubcate2 = ','.join(subcate2)
    sqlsubcate3 = ','.join(subcate3)
    sqlsubcate4 = ','.join(subcate4)

    sql10 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate10 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql11 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate11 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql12 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate12 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql13 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate13 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql14 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate14 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql15 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate15 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql16 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate16 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql17 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate17 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"

    sql2 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate2 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql3 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate3 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"
    sql4 = "select shopcode, pcode, pname, num, svalue, scost, gpvalue, gprate, closeqty, closevalue, cprice, price " \
          "from `kwsaletop10` " \
          "where classsx in (" + sqlsubcate4 + ") " \
                                                "and sdate='" + str(yesterday) + "' order by shopcode, svalue desc"

    # 连接数据库
    conn = mtu.getMysqlConn()
    cur10 = conn.cursor()
    cur11 = conn.cursor()
    cur12 = conn.cursor()
    cur13 = conn.cursor()
    cur14 = conn.cursor()
    cur15 = conn.cursor()
    cur16 = conn.cursor()
    cur17 = conn.cursor()
    cur2 = conn.cursor()
    cur3 = conn.cursor()
    cur4 = conn.cursor()
    cur10.execute(sql10)
    cur11.execute(sql11)
    cur12.execute(sql12)
    cur13.execute(sql13)
    cur14.execute(sql14)
    cur15.execute(sql15)
    cur16.execute(sql16)
    cur17.execute(sql17)
    cur2.execute(sql2)
    cur3.execute(sql3)
    cur4.execute(sql4)
    # 获取各部类下的销售数据
    rows10 = cur10.fetchall()
    rows11 = cur11.fetchall()
    rows12 = cur12.fetchall()
    rows13 = cur13.fetchall()
    rows14 = cur14.fetchall()
    rows15 = cur15.fetchall()
    rows16 = cur16.fetchall()
    rows17 = cur17.fetchall()
    rows2 = cur2.fetchall()
    rows3 = cur3.fetchall()
    rows4 = cur4.fetchall()

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows10)):
        for key in rows10[i].keys():
            row = rows10[i][key]
            if row is None:
                rows10[i][key] = ''
            else:
                if isinstance(row, int):
                    rows10[i][key] = str(rows10[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows10[i][key] = "%0.2f" % float(rows10[i][key])

    # 10 熟食部类
    lis10 = []
    unit10 =[]

    for sid in shopsid:
        i = 0
        for row in rows10:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis10.append(row)
                i += 1
            else:
                continue
        unit10.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows11)):
        for key in rows11[i].keys():
            row = rows11[i][key]
            if row is None:
                rows11[i][key] = ''
            else:
                if isinstance(row, int):
                    rows11[i][key] = str(rows11[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows11[i][key] = "%0.2f" % float(rows11[i][key])
    # 11 水产部类
    lis11 = []
    unit11 = []

    for sid in shopsid:
        i = 0
        for row in rows11:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis11.append(row)
                i += 1
            else:
                continue
        unit11.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows12)):
        for key in rows12[i].keys():
            row = rows12[i][key]
            if row is None:
                rows12[i][key] = ''
            else:
                if isinstance(row, int):
                    rows12[i][key] = str(rows12[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows12[i][key] = "%0.2f" % float(rows12[i][key])
    # 12 蔬菜部类
    lis12 = []
    unit12 = []

    for sid in shopsid:
        i = 0
        for row in rows12:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis12.append(row)
                i += 1
            else:
                continue
        unit12.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows13)):
        for key in rows13[i].keys():
            row = rows13[i][key]
            if row is None:
                rows13[i][key] = ''
            else:
                if isinstance(row, int):
                    rows13[i][key] = str(rows13[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows13[i][key] = "%0.2f" % float(rows13[i][key])
    # 13 烘烤部类
    lis13 = []
    unit13 = []

    for sid in shopsid:
        i = 0
        for row in rows13:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis13.append(row)
                i += 1
            else:
                continue
        unit13.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows14)):
        for key in rows14[i].keys():
            row = rows14[i][key]
            if row is None:
                rows14[i][key] = ''
            else:
                if isinstance(row, int):
                    rows14[i][key] = str(rows14[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows14[i][key] = "%0.2f" % float(rows14[i][key])
    # 14 鲜肉部类
    lis14 = []
    unit14 = []

    for sid in shopsid:
        i = 0
        for row in rows14:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis14.append(row)
                i += 1
            else:
                continue
        unit14.append(i)


    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows15)):
        for key in rows15[i].keys():
            row = rows15[i][key]
            if row is None:
                rows15[i][key] = ''
            else:
                if isinstance(row, int):
                    rows15[i][key] = str(rows15[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows15[i][key] = "%0.2f" % float(rows15[i][key])
    # 15 干鲜干果部类
    lis15 = []
    unit15 = []

    for sid in shopsid:
        i = 0
        for row in rows15:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis15.append(row)
                i += 1
            else:
                continue
        unit15.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows16)):
        for key in rows16[i].keys():
            row = rows16[i][key]
            if row is None:
                rows16[i][key] = ''
            else:
                if isinstance(row, int):
                    rows16[i][key] = str(rows16[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows16[i][key] = "%0.2f" % float(rows16[i][key])
    # 16 主食厨房部类
    lis16 = []
    unit16 = []

    for sid in shopsid:
        i = 0
        for row in rows16:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis16.append(row)
                i += 1
            else:
                continue
        unit16.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows17)):
        for key in rows17[i].keys():
            row = rows17[i][key]
            if row is None:
                rows17[i][key] = ''
            else:
                if isinstance(row, int):
                    rows17[i][key] = str(rows17[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows17[i][key] = "%0.2f" % float(rows17[i][key])
    # 17 水果部类
    lis17 = []
    unit17 = []

    for sid in shopsid:
        i = 0
        for row in rows17:
            if sid['ShopID'] == row['shopcode'] and i < 10:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis17.append(row)
                i += 1
            else:
                continue
        unit17.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows2)):
        for key in rows2[i].keys():
            row = rows2[i][key]
            if row is None:
                rows2[i][key] = ''
            else:
                if isinstance(row, int):
                    rows2[i][key] = str(rows2[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows2[i][key] = "%0.2f" % float(rows2[i][key])
    # 2 食品部类
    lis2 = []
    unit2 = []

    for sid in shopsid:
        i = 0
        for row in rows2:
            if sid['ShopID'] == row['shopcode'] and i < 20:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis2.append(row)
                i += 1
            else:
                continue
        unit2.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for i in range(0, len(rows3)):
        for key in rows3[i].keys():
            row = rows3[i][key]
            if row is None:
                rows3[i][key] = ''
            else:
                if isinstance(row, int):
                    rows3[i][key] = str(rows3[i][key])
                elif isinstance(row, decimal.Decimal):
                    rows3[i][key] = "%0.2f" % float(rows3[i][key])
    # 3 用品部类
    lis3 = []
    unit3 = []

    for sid in shopsid:
        i = 0
        for row in rows3:
            if sid['ShopID'] == row['shopcode'] and i < 20:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis3.append(row)
                i += 1
            else:
                continue
        unit3.append(i)

    # 判断当天是否有数据，同时转换数据类型 int 转 string, decimal 转 float
    for x in range(0, len(rows4)):
        for key in rows4[x].keys():
            row = rows4[x][key]
            if row is None:
                rows4[x][key] = ''
            else:
                if isinstance(row, int):
                    rows4[x][key] = str(rows4[x][key])
                elif isinstance(row, decimal.Decimal):
                    rows4[x][key] = "%0.2f" % float(rows4[x][key])

    # 将退货数据过滤，值为负
    rows4filter = []
    for i in range(0, len(rows4)):
        if float(rows4[i]['num']) < 0:
            continue
        else:
            rows4filter.append(rows4[i])

    # 4 家电部类
    lis4 = []
    templist = []

    for sid in shopsid:
        i = 0
        for row in rows4filter:
            if sid['ShopID'] == row['shopcode'] and i < 20:
                row['shopcode'] = sid['ShopName'].strip() + sid['ShopID']
                row['paiming'] = i + 1
                lis4.append(row)
                i += 1
            else:
                continue
        templist.append(i)


    # 关闭数据库
    mtu.close(conn, cur10)
    mtu.close(conn, cur11)
    mtu.close(conn, cur12)
    mtu.close(conn, cur13)
    mtu.close(conn, cur14)
    mtu.close(conn, cur15)
    mtu.close(conn, cur16)
    mtu.close(conn, cur17)
    mtu.close(conn, cur2)
    mtu.close(conn, cur3)
    mtu.close(conn, cur4)

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
    BasPurLog.objects.create(name="超市课组销售前十", url=path, qtype=qtype, ucode=ucode,uname=uname, createtime=today)

    if exceltype == '1':
        return export(request, lis10, lis11, lis12, lis13, lis14, lis15, lis16, lis17, lis2, lis3, lis4)
    else:
        return render(request, "report/daily/saletop10.html", locals())


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
    sql = "select distinct(classsx) from kwsaletop"
    cur.execute(sql)
    res = cur.fetchall()
    # 释放
    cur.close()
    lis = []

    for y in res:
        lis.append(y['classsx'])

    return lis


def export(request, lis10, lis11, lis12, lis13, lis14, lis15, lis16, lis17, lis2, lis3, lis4):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 写入sheet1
    writeDataToSheet1(wb, lis10)
    # 写入sheet2
    writeDataToSheet2(wb, lis11)
    # 写入sheet3
    writeDataToSheet3(wb, lis12)
    # 写入sheet4
    writeDataToSheet4(wb, lis13)
    # 写入sheet5
    writeDataToSheet5(wb, lis14)
    # 写入sheet6
    writeDataToSheet6(wb, lis15)
    # 写入sheet7
    writeDataToSheet7(wb, lis16)
    # 写入sheet8
    writeDataToSheet8(wb, lis17)
    # 写入sheet9
    writeDataToSheet9(wb, lis2)
    # 写入sheet10
    writeDataToSheet10(wb, lis3)
    # 写入sheet11
    writeDataToSheet11(wb, lis4)

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

    sheet10 = wb.add_sheet("10熟食", cell_overwrite_ok=True)

    titles = [
        [("（%s月%s日）各店日销售排名日报（熟食）" % (month, date.day), 0, 1, 13)],
        [("门店", 0, 2, 1), ("排名", 1, 2, 1), ("商品编码", 2, 2, 1), ("商品名称", 3, 2, 1), ("销售数量", 4, 2, 1),
         ("销售金额", 5, 2, 1), ("成本金额", 6, 2, 1), ("毛利", 7, 2, 1), ("毛利率%", 8, 2, 1), ("当前库存数量", 9, 2, 1),
         ("当前库存金额", 10, 2, 1), ("成本价", 11, 2, 1), ("平均售价", 12, 2, 1)],
    ]

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

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

    keylist = ['shopcode', 'paiming', 'pcode', 'pname', 'num', 'svalue', 'scost', 'gpvalue', 'gprate', 'closeqty', 'closevalue',
               'cprice', 'price']

    widthList = [600, 300, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600]

    # 日销售报表
    mtu.insertTitle2(sheet4, titles, keylist, widthList)
    mtu.insertCell2(sheet4, 3, lis4, keylist, None)
    titlesLen = len(titles)
    listTopLen = len(lis4)