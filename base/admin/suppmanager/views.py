# -*-coding:utf-8 -*-
__author__ = 'End-e'
from base.models import BasUser, BasUserRole, BasGroup
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ChangeGrpPass
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from base.utils import MethodUtil as mtu


@csrf_exempt
def change_passwd(request):
    posts = []
    if request.method == "POST":
        form = ChangeGrpPass(request.POST)
        grpcode = request.POST.get('grpcode')
        ucode = request.POST.get('ucode')
        passwd = request.POST.get('passwd')
        # confirmpass = request.POST.get('confirmpass')
        # if request.POST.get('action', None) == 'btnQuery':

        if request.POST.get('action', None) == 'btnSave':
             if form.is_valid():
                 user = BasUser.objects.get(ucode=ucode)
                 user.password =  mtu.md5(passwd)
                 user.save()

        sql = "select u.ucode, u.nm, u.grpcode, g.chnm as gnm from bas_user as u, bas_user_role as r,"
        sql += "bas_supplier as g where u.ucode = r.ucode and u.grpcode = g.suppcode and u.utype = '2' "
        sql += "and u.grpcode = '" + grpcode + "'"
        cursor = connection.cursor()
        cursor.execute(sql)
        rsobj = cursor.fetchall()
        # print(rsobj)
        for row in rsobj:
            post_dict = {}
            post_dict['ucode'] = row[0]
            post_dict['nm'] = row[1]
            post_dict['grpcode'] = row[2]
            post_dict['gnm'] = row[3]
            posts.append(post_dict)
    else:
        form = ChangeGrpPass()
    return render(request, 'admin/sysConf_supply_admin.html', {'form': form, 'posts': posts})
