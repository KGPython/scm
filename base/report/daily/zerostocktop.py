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

    #月份汇总数据
    sql = 'SElECT ShopID,shopname, SUM(qtyz) AS qtyzSum,SUM(qtyl) AS qtylSum,(sum(qtyl) / sum(qtyz)) AS zhonbiSum ' \
          'FROM Kzerostock ' \
          'WHERE sdate BETWEEN "'+monthFirst+'" AND "'+today+'" GROUP BY ShopID ORDER BY ShopID'
    cur = conn.cursor()
    cur.execute(sql)
    listRes= cur.fetchall()

    listTotal = {'ShopID':'合计','shopname':'','qtyzSum':0} #初始化最后一行
    #转换数据类型并求纵向合计
    for i in range(0,len(listRes)):
        if(not listRes[i]['qtyzSum']):
            listRes[i]['qtyzSum']=0
        listRes[i]['qtyzSum'] = float(listRes[i]['qtyzSum'])
        if 'qtyzSum' in listTotal:
            listTotal['qtyzSum'] += listRes[i]['qtyzSum']
        else:
            listTotal['qtyzSum'] = listRes[i]['qtyzSum']

        if(not listRes[i]['qtylSum']):
            listRes[i]['qtylSum']=0
        listRes[i]['qtylSum'] = float(listRes[i]['qtylSum'])
        if 'qtylSum' in listTotal:
            listTotal['qtylSum'] += listRes[i]['qtylSum']
        else:
            listTotal['qtylSum'] = listRes[i]['qtylSum']

        if(not listRes[i]['zhonbiSum']):
            listRes[i]['zhonbiSum']=0
        listRes[i]['zhonbiSum'] = float('%0.2f'%(listRes[i]['zhonbiSum']*100))
        listTotal['zhonbiSum'] = listTotal['qtylSum']/listTotal['qtyzSum']
        listTotal['zhonbiSum'] = str(float('%0.2f'%(listTotal['zhonbiSum']*100)))+'%'

        listTotal['mingciSum'] = ''

        sql = "SELECT b.sdate,SUM(b.qtyz) qtyz , SUM(b.qtyl) qtyl, (SUM(b.qtyl)/SUM(b.qtyz)) zhonbi, (SELECT COUNT(DISTINCT zhonbi) FROM Kzerostock a WHERE a.zhonbi <= b.zhonbi) AS mingci " \
              "FROM Kzerostock AS b " \
              "WHERE ShopID ='" + listRes[i]['ShopID'] +"' AND sdate BETWEEN '"+monthFirst+"' AND '"+today+"' GROUP BY sdate"
        cur.execute(sql)
        listDetail = cur.fetchall()

        for item in listDetail:
            date = str(item['sdate'])[8:10]
            if(not item['qtyz']):
                listRes[i]['qtyz_'+date]=0
            listRes[i]['qtyz_'+date]=float(item['qtyz'])
            if 'qtyz_'+date in listTotal:
                listTotal['qtyz_'+date] += listRes[i]['qtyz_'+date]
            else:
                listTotal['qtyz_'+date] = listRes[i]['qtyz_'+date]

            if(not item['qtyl']):
                listRes[i]['qtyl_'+date]=0
            listRes[i]['qtyl_'+date]=float(item['qtyl'])
            if 'qtyl_'+date in listTotal:
                listTotal['qtyl_'+date] += listRes[i]['qtyl_'+date]
            else:
                listTotal['qtyl_'+date] = listRes[i]['qtyl_'+date]

            if(not item['zhonbi']):
                listRes[i]['zhonbi_'+date]=0
            listRes[i]['zhonbi_'+date]=float('%0.2f'%(item['zhonbi']*100))
            listTotal['zhonbi_'+date] = listTotal['qtyl_'+date]/listTotal['qtyz_'+date]
            listTotal['zhonbi_'+date] = str(float('%0.2f'%(listTotal['zhonbi_'+date]*100)))+'%'

            listTotal['mingci_'+date] = ''

    # 排序生成总排名
    listRes = ranking(listRes,'zhonbiSum','mingciSum')
    # 排序生成每日排名
    for date in range(12,datetime.date.today().day+1):
        if(date<10):
            listRes = ranking(listRes,'zhonbi_0'+str(date),'mingci_0'+str(date))
        else:
            listRes = ranking(listRes,'zhonbi_'+str(date),'mingci_'+str(date))
    # 按门店排序
    listRes.sort(key=lambda x:x['ShopID'])
    return render(request,"report/daily/zero_stock_top.html",locals())

###
# 排名函数
# lis：需要排序的list
# key：排序的参照对象
# name:名次存放的字段名称
###
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