# -*- coding:utf-8 -*-
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

    sqlTop = 'SElECT ShopID,shopname, SUM(qtyz) AS qtyzSum,SUM(qtyl) AS qtylSum,(sum(qtyl) / sum(qtyz)) AS zhonbiSum ' \
          'FROM KNegativestock ' \
          'WHERE sdate BETWEEN "'+monthFirst+'" AND "'+today+'" GROUP BY ShopID ORDER BY ShopID'
    cur = conn.cursor()
    cur.execute(sqlTop)
    listRes= cur.fetchall()


    for i in range(0,len(listRes)):
        if(not listRes[i]['qtyzSum']):
            listRes[i]['qtyzSum']=0
        else:
            listRes[i]['qtyzSum'] = float(listRes[i]['qtyzSum'])
        if(not listRes[i]['qtylSum']):
            listRes[i]['qtylSum']=0
        else:
            listRes[i]['qtylSum'] = float(listRes[i]['qtylSum'])
        if(not listRes[i]['zhonbiSum']):
            listRes[i]['zhonbiSum']=0
        else:
            listRes[i]['zhonbiSum'] = float('%0.2f'%(listRes[i]['zhonbiSum']*100))

        sql = "SELECT b.sdate,SUM(b.qtyz) qtyz , SUM(b.qtyl) qtyl, (SUM(b.qtyl)/SUM(b.qtyz)) zhonbi, (SELECT COUNT(DISTINCT zhonbi) FROM KNegativestock a WHERE a.zhonbi <= b.zhonbi) AS mingci " \
              "FROM KNegativestock AS b " \
              "WHERE ShopID ='" + listRes[i]['ShopID'] +"' AND sdate BETWEEN '"+monthFirst+"' AND '"+today+"' GROUP BY sdate"

        cur.execute(sql)
        listDetail = cur.fetchall()
        for item in listDetail:
            date = str(item['sdate'])[8:10]
            if(not item['qtyz']):
                listRes[i]['qtyz_'+date]=0
            else:
                listRes[i]['qtyz_'+date]=float(item['qtyz'])
            if(not item['qtyl']):
                listRes[i]['qtyl_'+date]=0
            else:
                listRes[i]['qtyl_'+date]=float(item['qtyl'])
            if(not item['zhonbi']):
                listRes[i]['zhonbi_'+date]=0
            else:
                listRes[i]['zhonbi_'+date]=float('%0.2f'%(item['zhonbi']*100))
            listRes[i]['mingci_'+date]=item['mingci']

    listRes = ranking(listRes,'zhonbiSum','mingciSum')
    for date  in range(12,datetime.date.today().day+1):
        if(date<10):
            listRes = ranking(listRes,'zhonbi_0'+str(date),'mingci_0'+str(date))
        else:
            listRes = ranking(listRes,'zhonbi_'+str(date),'mingci_'+str(date))


    ###课组汇总###
    yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%y-%m-%d %H:%M:%S')
    sqlDept = 'select deptid,deptidname,sum(qtyz) qtyz,sum(qtyl) qtyl,(sum(qtyl)/sum(qtyz)) zhonbi from KNegativestock' \
          ' where sdate="'+yesterday+'" group by deptid,deptidname order by deptid'
    cur = conn.cursor()
    cur.execute(sqlDept)
    listDept = cur.fetchall()
    for obj in listDept:
        if(not obj['qtyz']):
            obj['qtyz'] = 0
        obj['qtyz'] = float(obj['qtyz'])
        if(not obj['qtyl']):
            obj['qtyl'] = 0
        obj['qtyl'] = float(obj['qtyl'])
        if(not obj['zhonbi']):
            obj['zhonbi'] = 0
        obj['zhonbi'] = str(float('%0.4f'%obj['zhonbi'])*100)[0:4]+'%'

    ###负库存课组明细###
    sqlDeptDetail = 'SELECT shopid,shopname,deptid,deptidname,qtyz,qtyl,zhonbi FROM KNegativestock WHERE sdate = "'\
          +str(yesterday)+'" GROUP BY deptid,shopid'
    cur = conn.cursor()
    cur.execute(sqlDeptDetail)
    listDeptDetail = cur.fetchall()
    for obj in listDeptDetail:
        if(not obj['zhonbi']):
            obj['zhonbi']= 0
        obj['zhonbi'] = str(float('%0.4f'%obj['zhonbi'])*100)[0:4]+'%'
        if(not obj['qtyl']):
            obj['qtyl']= 0
        obj['qtyl'] = float(obj['qtyl'])
        if(not obj['qtyz']):
            obj['qtyz']= 0
        obj['qtyz'] = float(obj['qtyz'])

    date = str(yesterday)[0:8]
    return render(request,"report/daily/negative_stock_top.html",locals())

def ranking(lis,key,name):
    """
    排名函数
    """
    # nums = [['a',11],['d',1],['g',34],['e',1],['h',35],['c',2],['i',37],['b',2],['f',1],['j',39]]

    # for obj in lis:
    #     for k in obj.keys():
    #         item = obj[k]
    #         if '%' in item :
    #             item =float(item[0:len(item)-1])

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
            # a[key] = str(a[key])+'%'
    return lis
