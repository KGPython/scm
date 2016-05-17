#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import MethodUtil
import datetime
from django.core import serializers

def index(request):
    #返回数据
    dataList = []

    conn = MethodUtil.getMysqlConn()
    start = str(datetime.date.today().replace(day=1))
    today = str(datetime.datetime.today())
    yesterday = str(datetime.datetime.today() - datetime.timedelta(days=1))
    #合计
    sqlSum = "select b.shopid,b.shopname,SUM(b.qtyz) AS qtyz,SUM(b.qtyl) AS qtyl,(SUM(b.qtyl)/SUM(b.qtyz)) AS zhonbi,(select count(distinct zhonbi) from Fcu_Stock a where a.zhonbi <= b.zhonbi) AS mingci from KNegativestock AS b WHERE stockdate BETWEEN '"+start+"' AND '"+today+"' GROUP BY shopid order by shopid"
    print(sqlSum)
    cur = conn.cursor()
    cur.execute(sqlSum)
    sumList = cur.fetchall()

    #将合计(横向)数据拼入数组
    for obj in sumList:
        list = []
        list.append(obj['shopid'])
        list.append(obj['shopname'])
        list.append(str(obj['qtyz']))
        list.append(str(obj['qtyl']))
        list.append(str(obj['zhonbi']))
        list.append(str(obj['mingci']))
        dataList.append(list)

    #求各门店明细并拼入数组
    dataLen = len(dataList)
    for i in range(0,dataLen):
        sql = "SELECT qtyz,qtyl,zhonbi,mingci FROM Fcu_Stock WHERE shopid ='"+sumList[i]['shopid']+"' ORDER BY stockdate"
        cur.execute(sql)
        list = cur.fetchall()

        for obj in list:
            dataList[i].append(str(obj['qtyz']))
            dataList[i].append(str(obj['qtyl']))
            dataList[i].append(str(obj['zhonbi']))
            dataList[i].append(str(obj['mingci']))
    #底部合计（纵向）
    sumList2 = []

    return render(request,'report/daily/negative_stock_top.html',{"dataList":dataList})

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass