# -*-  coding:utf-8 -*-
from django.shortcuts import render
from base.models import BasUser, RbacRoleInfo,RbacUserRole,RbacRole
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
        nm = request.POST.get('nm')
        password = '000000'
        status = request.POST.get('status')
        budate = request.POST.get('budate')
        uType = '3'
        res = {}
        try:
            BasUser.objects.create(ucode=ucode,nm=nm,password=password,utype=uType,status=status,budate=budate)
            res['msg'] = 0
        except Exception as e:
            print(e)
            res['msg']=1
    return render(request,'rbac/user/create.html',locals())

def delete(request):
    pass

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



