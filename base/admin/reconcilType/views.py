__author__ = 'Administrator'
from django.shortcuts import render
from base.utils import MethodUtil
def reconcilType(request):
    #复选框列表
    conn = MethodUtil.getMssqlTranConn()

    sqlPayList = "select id,name from paytype"
    conn.execute_query(sqlPayList)
    PayList = [ row for row in conn ]

    conn2 = MethodUtil.getMysqlConn()
    conn2.autocommit(True)
    #对账方式列表（页面左部）
    sqlRec = "select id,rname from reconcil where status='1'"
    print(sqlRec)
    curSel = conn2.cursor()
    try:
        curSel.execute(sqlRec)
    except Exception as e:
        print(e)
    recList = curSel.fetchall()
    action = request.GET.get('action','')
    if request.method == 'POST':
        if action == 'new':
            reconName = request.POST.get('reconName')
            payTyleList = request.POST.getlist('payType')
            sqlNew1 = "insert into reconcil (rname,status) values('{name}')".format(name=reconName)

            try:
                curNew1 = conn2.cursor()
                curNew1.execute(sqlNew1)
                curNew1.close()
            except Exception as e:
                print(e)
            sqlNew2 = "select id from reconcil where rname='{rname}'".format(rname=reconName)
            curNew2 = conn2.cursor()
            curNew2.execute(sqlNew2)
            rid = curNew2.fetchone()

            curNew2.close()

            curNew3 = conn2.cursor()
            for payTpye in payTyleList:
                sqlNew3 = "insert into reconcilitem (rid,pid) values({rid},{pid})".format(rid=int(rid['id']),pid=int(payTpye))
                try:
                    curNew3.execute(sqlNew3)
                except Exception as e:
                    print(e)
            curNew3.close()
            conn2.close()
        elif action == 'edit':
            #获取修改项目名称
            reconName = request.POST.get('reconName')
            payTyleList = request.POST.getlist('payType')

            #获取修改项目id
            sqlEdit1 = "select id from reconcil where rname='{rname}'".format(rname=reconName)
            curEdit1 = conn2.cursor()
            curEdit1.execute(sqlEdit1)
            rid = curEdit1.fetchone()
            curEdit1.close()
            #删除相关信息
            sqlEdit2 = "delete from reconcilitem where rid={rid}".format(rid=int(rid['id']))
            curEdit2 = conn2.cursor()
            curEdit2.execute(sqlEdit2)
            curEdit2.close()

            curEdit3 = conn2.cursor()
            for payTpye in payTyleList:
                sqlEdit3 = "insert into reconcilitem (rid,pid) values({rid},{pid})".format(rid=int(rid['id']),pid=int(payTpye))
                curEdit3.execute(sqlEdit3)

    return render(request,'admin/reconcilType.html',locals())