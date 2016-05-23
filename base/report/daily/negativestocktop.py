# -*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import MethodUtil
import datetime
from django.core import serializers


def index(request):
    # 返回数据
    dataList = []

    conn = MethodUtil.getMysqlConn()
    start = str(datetime.date.today().replace(day=1))
    today = str(datetime.datetime.today())
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    # 合计
    sql = "select ShopID, shopname, " \
          "sum(qtyz) as qtyz, " \
          "sum(qtyl) as qtyl, " \
          "(sum(qtyl) / sum(qtyz)) as zhonbi " \
          "from KNegativestock " \
          "where sdate between '" + start + "' and '" + today + \
          "' group by ShopID " \
          "order by ShopID asc "
    cur = conn.cursor()
    cur.execute(sql)
    sumList = cur.fetchall()

    print(sumList)

    try:
        if (sumList):
            pass
    except:
        pass

    print(sumList)

    # 将合计(横向)数据拼入数组
    for obj in sumList:
        list = []
        list.append(obj['ShopID'])
        list.append(obj['shopname'])
        # qtyz 有效商品数
        list.append(str(obj['qtyz']))
        # qtyl 合计
        list.append(str(obj['qtyl']))
        # zhonbi  占比
        list.append(format(obj['zhonbi'] * 100, '0.2f'))
        # list.append(format((obj['zhonbi']), '0.2%'))
        dataList.append(list)

    # 调用ranking()函数对占比进行排名
    dataList = ranking(dataList)

    # 再调整排序，按照ShopID
    dataList.sort()
    # print(dataList)

    # 求各门店明细并拼入数组
    # dataLen = len(dataList)
    # for i in range(0, dataLen):
    #     sql = "SELECT b.ShopID, b.sdate, b.qtyz, b.qtyl, b.zhonbi, (SELECT COUNT(DISTINCT zhonbi) FROM KNegativestock a WHERE a.zhonbi <= b.zhonbi) AS mingci " \
    #           "FROM KNegativestock AS b " \
    #           "WHERE ShopID ='" + sumList[i]['ShopID'] + \
    #           "' ORDER BY sdate"
    #     print(sql)
    #     cur.execute(sql)
    #     list = cur.fetchall()
    #
    #     for obj in list:
    #         dataList[i].append(str(obj['qtyz']))
    #         dataList[i].append(str(obj['qtyl']))
    #         dataList[i].append(str(obj['zhonbi']))
    #         dataList[i].append(str(obj['mingci']))
    # 底部合计（纵向）
    # sumList2 = []

    return render(request, 'report/daily/negative_stock_top.html', {"dataList": dataList})


@csrf_exempt
def query():
    pass


@csrf_exempt
def download():
    pass


def ranking(lis):
    """
    排名函数
    """
    # nums = [['a',11],['d',1],['g',34],['e',1],['h',35],['c',2],['i',37],['b',2],['f',1],['j',39]]
    lis.sort(key=lambda x:x[4])
    j = 1
    for i in range(0,len(lis)):
        if i > 0:
            a = lis[i-1]
            b = lis[i]
            if float(a[4]) != float(b[4]):
                j += 1
            b.append(j)
        else:
            a = lis[i]
            a.append(j)
    return lis
