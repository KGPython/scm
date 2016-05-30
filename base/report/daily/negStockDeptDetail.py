# -*- coding:utf-8 -*-
__author__ = 'chen'
import datetime
from django.shortcuts import render
from base.utils import MethodUtil

def index(request):
    conn = MethodUtil.getMysqlConn()
    yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%y-%m-%d %H:%M:%S')
    sql = 'SELECT shopid,shopname,deptid,deptidname,qtyz,qtyl,zhonbi FROM KNegativestock WHERE sdate = "'\
          +str(yesterday)+'" GROUP BY deptid,shopid'
    cur = conn.cursor()
    cur.execute(sql)
    listDeptDetail = cur.fetchall()
    for obj in list:
        if(not obj['zhonbi']):
            obj['zhonbi']= 0
        obj['zhonbi'] = str(float('%0.4f'%obj['zhonbi'])*100)[0:4]+'%'
        if(not obj['qtyl']):
            obj['qtyl']= 0
        obj['qtyl'] = float(obj['qtyl'])
        if(not obj['qtyz']):
            obj['qtyz']= 0
        obj['qtyz'] = float(obj['qtyz'])


    conn.close()
    cur.close()
    date = str(yesterday)[0:8]
    return render(request,'report/daily/negative_stock_top.html',locals())
