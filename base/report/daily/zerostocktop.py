#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from base.utils import MethodUtil

@csrf_exempt
def index(request):
    monthFirst = str(datetime.date.today().replace(day=1))
    today = str(datetime.datetime.today().strftime('%y-%m-%d'))
    conn = MethodUtil.getMysqlConn()

    sql = 'SElECT ShopID,shopname, SUM(qtyz) AS qtyz,SUM(qtyl) AS qtyl,(sum(qtyl) / sum(qtyz)) AS zhonbi ' \
          'FROM Kzerostock ' \
          'WHERE sdate BETWEEN "'+monthFirst+'" AND "'+today+'" GROUP BY ShopID ORDER BY ShopID'
    cur = conn.cursor();
    cur.execute(sql)
    listSum = cur.fetchall()

    for obj in listSum:
        sql = "SELECT b.sdate,b.qtyz, b.qtyl, b.zhonbi, (SELECT COUNT(DISTINCT zhonbi) FROM KNegativestock a WHERE a.zhonbi <= b.zhonbi) AS mingci " \
              "FROM Kzerostock AS b " \
              "WHERE ShopID ='" + obj['ShopID'] + \
              "' ORDER BY sdate"
        cur.execute(sql)
        listDetail = cur.fetchall()
        # for item in listDetail:
        #     date = item['sdate'][7:9]
    return render(request,"report/daily/zero_stock_top.html",locals())

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass