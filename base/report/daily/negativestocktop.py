#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import MethodUtil
import time,datetime

@csrf_exempt
def index(request):
    conn = MethodUtil.getMysqlConn()
    start = str(datetime.date.today().replace(day=1))
    end = str(datetime.datetime.today())

    #合计
    sqlSum = "select shopid,shopname,SUM(qtyz) AS qtyz,SUM(qtyl) AS qtyl,(SUM(qtyl)/SUM(qtyz)) AS zhonbi from Fcu_Stock WHERE stockdate BETWEEN '"+start+"' AND '"+end+"' GROUP BY shopid order by shopid"
    cur = conn.cursor()
    cur.execute(sqlSum)
    sumList = cur.fetchall()

    dataList = []
    for obj in sumList:
        list = []
        list.append(obj)
        dataList.append(list)

    mingci = 1
    dataLen = len(dataList)
    mxList =[]
    for i in range(0,dataLen):
        sql = "SELECT qtyz,qtyl,zhonbi,mingci FROM Fcu_Stock WHERE shopid ='"+sumList[i]['shopid']+"'"
        cur.execute(sql)
        list = cur.fetchall()
        dataList[i].append(list)

        # sumList[i]['mingci'] = mingci
        # if sumList[i]['zhonbi'] <= sumList[i-1]['zhonbi']:
        #     mingci += 1
        #     sumList[i]['mingci'] = mingci

    print(dataList)
    return render(request,'report/daily/negative_stock_top.html',locals())

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass