# -*-  coding:utf-8 -*-
from django.shortcuts import render
from base.models import BasUser,RbacUserRole,RbacRole
from django.http import HttpResponse
import json



def index(request):
    users = BasUser.objects.values('ucode','nm','status','budate').filter(utype='3')
    return render(request,'rbac/user/index.html',locals())

def create(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        user = BasUser.objects.values('ucode','nm','status','budate').filter(ucode=id).first()
    if request.method == 'POST':
        ucode = request.POST.get('ucode')
        nm = request.POST.get('name')
        status = request.POST.get('status')
        budate = request.POST.get('budate')
        action = request.POST.get('action')
        res = {}
        try:
            if action == 'edit':
                res_update = BasUser.objects.filter(ucode=ucode).update(nm=nm,status=status, budate=budate)
            else:
                password = '000000'
                uType = '3'
                BasUser.objects.create(ucode=ucode,nm=nm,password=password,utype=uType,status=status,budate=budate)
            res['msg'] = 0
        except Exception as e:
            print(e)
            res['msg']=1
    return render(request,'rbac/user/create.html',locals())

def delete(request):
    id = request.GET.get('id')
    res = {}
    if id:
        res_del = BasUser.objects.filter(ucode=id).delete()
        if not res_del[0]:
            res['msg'] = 1
        res['msg'] = 0
    else:
        res['msg'] = 1

    return HttpResponse(json.dumps(res))

def info(request):
    res = {}
    if request.method == 'GET':
        ucode = request.GET.get('id')
        info = RbacUserRole.objects.values('role').filter(user_id=ucode).first()
        roles = RbacRole.objects.values('role_id','role_name').filter(status=0)
    if request.method == 'POST':
        ucode = request.POST.get('ucode')
        role = request.POST.get('role')
        userRole = RbacUserRole.objects.filter(user_id=ucode)
        try:
            if userRole.count():
                userRole.update(role=role)
            else:
                userRole = RbacUserRole()
                userRole.role = role
                userRole.user_id = ucode
                userRole.save()
            res['msg'] = 0
        except Exception as e:
            print(e)
            res['msg'] = 1
    return render(request, 'rbac/user/userInfo.html', locals())



