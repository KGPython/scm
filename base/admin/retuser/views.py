#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from base.models import BasUser,BasUserRole,BasRole,BasKe
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base.utils import Constants,MethodUtil as mtu
import datetime,json

LIMIT = 3

@csrf_exempt
def index(request):
    grpcode = request.session.get('s_grpcode','')
    utype = request.session.get("s_utype")
    page = mtu.getReqVal(request,"page","1")

    action = mtu.getReqVal(request,"action")

    nm = mtu.getReqVal(request,"nm")
    ucode = mtu.getReqVal(request,"ucode")
    pwd = mtu.getReqVal(request,"pwd")
    dept = mtu.getReqVal(request,"dept")
    status = mtu.getReqVal(request,"status")
    remark = mtu.getReqVal(request,"remark")

    user = BasUser()
    if action!="new":
        try:
            user = BasUser.objects.get(ucode=ucode)
        except:
           user = None

        if action == "save":
            if not user:
                user = BasUser()
                user.ucode = ucode
                user.budate = datetime.date.today()

            user.password = mtu.md5(pwd)
            user.nm = nm
            user.dept = dept
            user.utype = utype
            user.status = status
            user.remark = remark
            user.grpcode = grpcode
            user.save()

            ke = BasKe()
            ke.kbcode = user.ucode
            ke.kbname = user.nm
            ke.save()
        elif action == "del":
            try:
                ke = BasKe.objects.get(kbcode=ucode)
                if ke:
                    ke.delete()
            except Exception as e:
               print(e)
            if user:
                user.delete()
            user = BasUser()

    retUserList = BasUser.objects.values('ucode','nm','password','dept','depttype','utype','status','grpcode').filter(grpcode=grpcode)
    paginator = Paginator(retUserList,LIMIT)
    try:
        retUserList = paginator.page(int(page))
    except Exception as e:
        print(e)
        retUserList = []

    pageCount = paginator.num_pages
    pageList = []
    for index in range(1,pageCount+1):
        pageList.append(index)
    usertype = (str(utype),Constants.USER_TYPE.get(utype))

    rs = {}
    rs["page"] = page
    rs["usertype"] = usertype
    rs["retUserList"] = retUserList
    rs["pageList"] = pageList
    rs["grpcode"] = grpcode
    rs["user"] = user
    return render(request,'admin/sysConf_retail_admin.html',rs)

@csrf_exempt
def findrole(request):
    grpcode = request.session.get("s_grpcode")
    utype = request.session.get("s_utype")
    ucode = mtu.getReqVal(request,"ucode")

    urlist = BasUserRole.objects.filter(ucode=ucode).values("rcode")
    rlist = BasRole.objects.filter(grpcode__in=[utype,grpcode]).values()

    rs = {}
    rs["rlist"]=[dict(row) for row in rlist]
    rs["urlist"]=[row["rcode"] for row in urlist]
    return HttpResponse(json.dumps(rs))

@csrf_exempt
def saverole(request):
    ucode = mtu.getReqVal(request,"ucode")
    rlist = request.POST.getlist("rcode")
    rs = {}
    try:
        cursor = connection.cursor()
        sql = "delete from bas_user_role where ucode=" + ucode
        cursor.execute(sql)
        for row in rlist:
            sql = "insert into bas_user_role(ucode, rcode, status,brdate) values ('" + ucode + "','" + row + "', 0, curdate())"
            cursor.execute(sql)
        rs["status"] = '0'
    except Exception as e:
        print(e)
        rs["status"] = '1'
    return HttpResponse(json.dumps(rs))

