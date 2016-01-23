# -*- coding:utf-8 -*-
# __author__ = 'Administrator'

from django.shortcuts import render
from base.utils import MethodUtil
from django.http import HttpResponseRedirect

def reconcilType(request):
    #复选框列表

    conn2 = MethodUtil.getMysqlConn()
    conn2.autocommit(True)
    cur=conn2.cursor()
    sqlPayList = "select id,name from bas_paytype"
    cur.execute(sqlPayList)
    PayList = cur.fetchall()



    #对账方式列表（页面左部）
    QsqlRec = "select id,rname from reconcil where status='1'"
    QcurSel = conn2.cursor()
    QcurSel.execute(QsqlRec)
    QrecList = QcurSel.fetchall()

    JsqlRec = "select id,rname from reconcil where status='0'"
    JcurSel = conn2.cursor()
    JcurSel.execute(JsqlRec)
    JrecList = JcurSel.fetchall()

    action = request.GET.get('action','')
    if request.method == 'POST':
        reconName = request.POST.get('reconName')
        rstatus =  request.POST.get('rstatus')
        payTyleList = request.POST.getlist('payType')
        if action == 'new':
            try:
                sqlNew1 = "insert into reconcil (rname,status) values('{name}','{status}')".format(name=reconName,status=rstatus)
                curNew1 = conn2.cursor()
                print(sqlNew1)
                curNew1.execute(sqlNew1)
                curNew1.close()

                sqlNew2 = "select id from reconcil where rname='{rname}'".format(rname=reconName)
                curNew2 = conn2.cursor()
                curNew2.execute(sqlNew2)
                rid = curNew2.fetchone()
                curNew2.close()

                curNew3 = conn2.cursor()
                for payTpye in payTyleList:
                    sqlNew3 = "insert into reconcilitem (rid,pid) values({rid},'{pid}')".format(rid=int(rid['id']),pid=payTpye)
                    curNew3.execute(sqlNew3)
                curNew3.close()
                conn2.close()
                succ = True
            except:
                succ = False
        elif action == 'edit':
            #获取修改项目名称
            rid = request.POST.get('reconId')
            try:
                #更新reconcil数据
                sqlEdit1 = "update reconcil set rname='{rname}',status='{rstatus}' where id={id}"\
                            .format(rname=reconName,rstatus=rstatus,id=rid)
                curEdit1 = conn2.cursor()
                curEdit1.execute(sqlEdit1)
                curEdit1.close()
                #删除相关信息
                sqlEdit2 = "delete from reconcilitem where rid={rid}".format(rid=rid)
                curEdit2 = conn2.cursor()
                curEdit2.execute(sqlEdit2)
                curEdit2.close()

                curEdit3 = conn2.cursor()
                for payTpye in payTyleList:
                    sqlEdit3 = "insert into reconcilitem (rid,pid) values({rid},'{pid}')".format(rid=rid,pid=payTpye)
                    curEdit3.execute(sqlEdit3)
                succ = True
            except:
                succ = False
    else:
        rid = request.GET.get('rid','')
        if rid:
            sqlShow1="select id,rname,status from reconcil where id={rid}".format(rid=rid)
            curShow1 = conn2.cursor()
            curShow1.execute(sqlShow1)
            reconList = curShow1.fetchone()

            sqlShow2 = "select pid from reconcilitem where rid={rid}".format(rid=rid)
            curShow2 = conn2.cursor()
            curShow2.execute(sqlShow2)
            payTyleLoad = curShow2.fetchall()
            print(payTyleLoad)

    return render(request,'admin/reconcilType.html',locals())