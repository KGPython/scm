#-*- coding:utf-8 -*-
__author__ = ''

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from base.utils import MethodUtil as mtu

@csrf_exempt
def index(request):
    ###门店排名###
    monthFirst = str(datetime.date.today().replace(day=1))
    today = str(datetime.datetime.today().strftime('%y-%m-%d'))
    lastMonthFirst = datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)
    lastMonthEnd = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)
    # 修正每个月1号的查询条件
    if(today[7:8]=='01'):
        monthFirst = str(lastMonthFirst.strftime('%y-%m-%d'))
        today = str(lastMonthEnd.strftime('%y-%m-%d'))
    conn = mtu.getMysqlConn()

    #月份汇总数据
    sqlTop = 'SElECT ShopID,shopname, SUM(qtyz) AS qtyzSum,SUM(qtyl) AS qtylSum,(sum(qtyl) / sum(qtyz)) AS zhonbiSum ' \
          'FROM Kzerostock ' \
          'WHERE sdate BETWEEN "'+monthFirst+'" AND "'+today+'" GROUP BY ShopID ORDER BY ShopID'
    cur = conn.cursor()
    cur.execute(sqlTop)
    listTop = cur.fetchall()
    listTotal = {'ShopID':'合计','shopname':'','qtyzSum':0} #初始化最后一行
    #转换数据类型并求纵向合计
    for i in range(0,len(listTop)):
        if(not listTop[i]['qtyzSum']):
            listTop[i]['qtyzSum']=0
        else:
            listTop[i]['qtyzSum'] = float(listTop[i]['qtyzSum'])
        if 'qtyzSum' in listTotal:
            listTotal['qtyzSum'] += listTop[i]['qtyzSum']
        else:
            listTotal['qtyzSum'] = listTop[i]['qtyzSum']

        if(not listTop[i]['qtylSum']):
            listTop[i]['qtylSum']=0
        else:
            listTop[i]['qtylSum'] = float(listTop[i]['qtylSum'])
        if 'qtylSum' in listTotal:
            listTotal['qtylSum'] += listTop[i]['qtylSum']
        else:
            listTotal['qtylSum'] = listTop[i]['qtylSum']

        if(not listTop[i]['zhonbiSum']):
            listTop[i]['zhonbiSum']=0
        else:
            listTop[i]['zhonbiSum'] = float('%0.2f'%(listTop[i]['zhonbiSum']*100))
        listTotal['zhonbiSum'] = listTotal['qtylSum']/listTotal['qtyzSum']
        listTotal['zhonbiSum'] = str(float('%0.2f'%(listTotal['zhonbiSum']*100)))+'%'

        listTotal['mingciSum'] = ''

        sql = "SELECT b.sdate,SUM(b.qtyz) qtyz , SUM(b.qtyl) qtyl, (SUM(b.qtyl)/SUM(b.qtyz)) zhonbi, (SELECT COUNT(DISTINCT zhonbi) FROM Kzerostock a WHERE a.zhonbi <= b.zhonbi) AS mingci " \
              "FROM Kzerostock AS b " \
              "WHERE ShopID ='" + listTop[i]['ShopID'] +"' AND sdate BETWEEN '"+monthFirst+"' AND '"+today+"' GROUP BY sdate"
        cur.execute(sql)
        listDetail = cur.fetchall()

        for item in listDetail:
            date = str(item['sdate'])[8:10]
            if(not item['qtyz']):
                listTop[i]['qtyz_'+date]=0
            else:
                listTop[i]['qtyz_'+date]=float(item['qtyz'])
            if 'qtyz_'+date in listTotal:
                listTotal['qtyz_'+date] += listTop[i]['qtyz_'+date]
            else:
                listTotal['qtyz_'+date] = listTop[i]['qtyz_'+date]

            if(not item['qtyl']):
                listTop[i]['qtyl_'+date]=0
            else:
                listTop[i]['qtyl_'+date]=float(item['qtyl'])
            if 'qtyl_'+date in listTotal:
                listTotal['qtyl_'+date] += listTop[i]['qtyl_'+date]
            else:
                listTotal['qtyl_'+date] = listTop[i]['qtyl_'+date]

            if(not item['zhonbi']):
                listTop[i]['zhonbi_'+date]=0
            else:
                listTop[i]['zhonbi_'+date]=float('%0.2f'%(item['zhonbi']*100))
            listTotal['zhonbi_'+date] = listTotal['qtyl_'+date]/listTotal['qtyz_'+date]
            listTotal['zhonbi_'+date] = str(float('%0.2f'%(listTotal['zhonbi_'+date]*100)))+'%'

            listTotal['mingci_'+date] = ''

    # 排序生成总排名
    listTop = ranking(listTop,'zhonbiSum','mingciSum')
    # 排序生成每日排名
    for date in range(12,datetime.date.today().day+1):
        if(date<10):
            listTop = ranking(listTop,'zhonbi_0'+str(date),'mingci_0'+str(date))
        else:
            listTop = ranking(listTop,'zhonbi_'+str(date),'mingci_'+str(date))
    # 按门店排序
    listTop.sort(key=lambda x:x['ShopID'])

    ###课组汇总###
    yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%y-%m-%d %H:%M:%S')
    sqlDept = 'select deptid,deptidname,sum(qtyz) qtyz,sum(qtyl) qtyl,(sum(qtyl)/sum(qtyz)) zhonbi from KNegativestock' \
          ' where sdate="'+yesterday+'" group by deptid,deptidname order by deptid'
    cur = conn.cursor()
    cur.execute(sqlDept)
    listDept = cur.fetchall()
    for obj in list:
        if(not obj['qtyz']):
            obj['qtyz'] = 0
        obj['qtyz'] = float(obj['qtyz'])
        if(not obj['qtyl']):
            obj['qtyl'] = 0
        obj['qtyl'] = float(obj['qtyl'])
        if(not obj['zhonbi']):
            obj['zhonbi'] = 0
        obj['zhonbi'] = str(float('%0.4f'%obj['zhonbi'])*100)[0:4]+'%'
    date = str(yesterday)[0:8]
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