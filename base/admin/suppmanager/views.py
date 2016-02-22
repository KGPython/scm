# -*-coding:utf-8 -*-
__author__ = 'End-e'
import json
from base.models import BasUser
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ChangeGrpPass
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from base.utils import MethodUtil as mtu


@csrf_exempt
def query_supp(request):
    posts = []
    grpcode = mtu.getReqVal(request,"grpcode","")
    if grpcode:
        sql = "select u.ucode, u.nm, u.grpcode, g.chnm as gnm from bas_user as u,"
        sql += "bas_supplier as g where u.grpcode = g.suppcode and u.utype = '2' "
        sql += "and u.grpcode like '%" + grpcode.strip() + "%'"
        cursor = connection.cursor()
        cursor.execute(sql)
        rsobj = cursor.fetchall()
        for row in rsobj:
            post_dict = {}
            post_dict['ucode'] = row[0]
            post_dict['nm'] = row[1]
            post_dict['grpcode'] = row[2]
            post_dict['gnm'] = row[3]
            posts.append(post_dict)
    form = ChangeGrpPass()
    return render(request, 'admin/sysConf_supply_admin.html', {'form': form, 'posts': posts,"grpcode":grpcode})

@csrf_exempt
def update_pwd(request):
    rs = {}
    ucode = request.POST.get('ucode')
    passwd = request.POST.get('passwd')
    try:
        user = BasUser.objects.get(ucode=ucode)
        user.password =  mtu.md5(passwd)
        user.save()
        rs["status"] = "0"
    except Exception as e:
        rs["status"] = "1"
        print(e)
    return HttpResponse(json.dumps(rs))
