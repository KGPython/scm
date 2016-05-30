# -*- coding:utf-8 -*-
__author__ = 'chen'

from django.shortcuts import render
import datetime
from base.utils import MethodUtil

def index(request):
    yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%y-%m-%d %H:%M:%S')
    conn = MethodUtil.getMysqlConn()
    sql = 'select deptid,deptidname,sum(qtyz) qtyz,sum(qtyl) qtyl,(sum(qtyl)/sum(qtyz)) zhonbi from Kzerostock' \
          ' where sdate="'+yesterday+'" group by deptid,deptidname order by deptid'
    cur = conn.cursor()
    cur.execute(sql)
    list = cur.fetchall()
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
    cur.close()
    conn.close()
    return render(request, 'report/daily/aero_stock_dept.html',locals())