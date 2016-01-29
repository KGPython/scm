# -*- coding:utf-8 -*-
# __author__ = 'Administrator'

import datetime
from django.shortcuts import render
from base.utils import MethodUtil
from django.http import HttpResponseRedirect

def reconcilType(request):
    #复选框列表
    conn2 = MethodUtil.getMysqlConn()
    conn2.autocommit(True)
    cur=conn2.cursor()
    sqlPayList = "select id,name from bas_paytype order by name desc"
    cur.execute(sqlPayList)
    PayList = cur.fetchall()

    #对账方式列表（页面左部）
    QsqlRec = "select id,rname from reconcil where status='1' order by rname"
    cur.execute(QsqlRec)
    QrecList = cur.fetchall()

    JsqlRec = "select id,rname from reconcil where status='0' order by rname"
    cur.execute(JsqlRec)
    JrecList = cur.fetchall()

    #
    rid = request.GET.get('rid','')
    if rid:
        sqlShow1="select id,rname,status,beginday,endday from reconcil where id={rid}".format(rid=rid)
        curShow1 = conn2.cursor()
        curShow1.execute(sqlShow1)
        reconList = curShow1.fetchone()

        sqlShow2 = "select pid from reconcilitem where rid={rid}".format(rid=rid)
        curShow2 = conn2.cursor()
        curShow2.execute(sqlShow2)
        payTyleLoad = curShow2.fetchall()
    else:
        today = datetime.date.today()
        currmonth = MethodUtil.getCurrentMonthDay(today)
        if today.day <= 15:
            reconList = {"beginday":"1","endday":"15"}
        else:
            reconList = {"beginday":"16","endday":"{end}".format(end=currmonth[2])}
        payTyleLoad = []
    #新建、修改、删除
    action = request.GET.get('action','')
    if request.method == 'POST':
        reconName = request.POST.get('reconName')
        rstatus =  request.POST.get('rstatus')
        beginday = request.POST.get('beginday')
        endday = request.POST.get('endday')
        payTyleList = request.POST.getlist('payType')
        rid = request.POST.get('reconId')

        if action == 'save':
            #修改
            if rid:
                try:
                    #更新reconcil数据
                    sqlEdit1 = "update reconcil set rname='{rname}',status='{rstatus}',beginday={beginday},endday={endday} where id={id}"\
                                .format(rname=reconName,rstatus=rstatus,id=rid,endday=endday,beginday=beginday)
                    cur.execute(sqlEdit1)

                    #删除相关信息
                    sqlEdit2 = "delete from reconcilitem where rid={rid}".format(rid=rid)
                    cur.execute(sqlEdit2)

                    for payTpye in payTyleList:
                        sqlEdit3 = "insert into reconcilitem (rid,pid) values({rid},'{pid}')".format(rid=rid,pid=payTpye)
                        cur.execute(sqlEdit3)

                    cur.close()
                    conn2.close()
                    succ = True
                except:
                    succ = False
            #保存
            else:
                try:
                    sqlNew1 = "insert into reconcil (rname,status,beginday,endday) values('{name}','{status}',{beginday},{endday})"\
                        .format(name=reconName,status=rstatus,beginday=beginday,endday=endday)
                    cur.execute(sqlNew1)

                    rid = cur.lastrowid
                    for payTpye in payTyleList:
                        sqlNew3 = "insert into reconcilitem (rid,pid) values({rid},'{pid}')".format(rid=int(rid),pid=payTpye)
                        cur.execute(sqlNew3)

                    cur.close()
                    conn2.close()
                    succ = True
                except:
                    succ = False
        #删除
        elif action == 'del':
            try:
                rid = request.POST.get('reconId')
                sqlDel1 = "delete from reconcil where id={id}".format(id=rid)
                cur.execute(sqlDel1)

                sqlDel2 = "delete from reconcilitem where rid={rid}".format(rid=rid)
                cur.execute(sqlDel2)

                succ = True
                cur.close()
                conn2.close()
            except:
                succ = False


    dayList = [n for n in range(1,32)]
    return render(request,'admin/reconcilType.html',locals())