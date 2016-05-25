# -*-coding:utf-8 -*-
__author__ = 'End-e'
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from base.models import BasRole, BasUserRole, BasRolePur, BasPur
from .forms import RoleForm  # 引入创建的表单类
from django.db import connection
import json
# 引入分页
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

limit = 10

def index(request):
    form = RoleForm()
    # 分页
    topics = BasRole.objects.filter(grpcode="2")
    paginator = Paginator(topics, limit)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'admin/sysConf_supply.html', {'form': form, 'topics': topics, 'page': page})


@csrf_exempt
def add_form(request):
    page = request.POST.get("page")
    flag = 0

    # 查询列表
    topics = BasRole.objects.filter(grpcode="2")
    paginator = Paginator(topics, limit)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    # 编辑
    if request.method == 'POST':  # 当提交表单时
        rcode = request.POST.get('rcode')
        oldrcode = request.POST.get('oldrcode')
        try:
            role = BasRole.objects.get(rcode=rcode)
        except:
            role = None
        # 添加 修改
        if request.POST.get('action', None) == 'saveQuery':  # 保存数据
            form = RoleForm(request.POST)  # from 包含提交的数据
            if form.is_valid():  # 如果提交的数据合法
                nm = form.cleaned_data['nm']
                status = form.cleaned_data['status']
                remark = form.cleaned_data['remark']
                grpcode = form.cleaned_data['grpcode']
            if oldrcode and role:
                # 修改
                role.nm = nm
                role.status = status
                role.remark = remark
                role.grpcode = grpcode
                role.save()
            if not oldrcode and not role:
                # 添加
                BasRole.objects.create(nm=nm, rcode=rcode, status=status, remark=remark, grpcode=grpcode)
            if not oldrcode and role:
                flag = 1
        # 删除
        if request.POST.get('action', None) == 'delQuery':  # 删除数据
            role.delete()
            form = RoleForm()

    # 查询
    elif request.method == 'GET':
        page = request.GET.get('page')
        rcode = request.GET.get('rcode')
        role = BasRole.objects.values("rcode", "nm", "status", "remark", "grpcode").get(rcode=rcode)
        form = RoleForm(role)
        form.is_valid()

    else:  # 当正常访问时
        form = RoleForm()

    return render(request, 'admin/sysConf_supply.html',
                  {'form': form, 'rcode': rcode, 'page': page, 'topics': topics, 'flag': flag})


@csrf_exempt
def queryRole(request):
    purL = []
    uPurL = []
    rcode = request.POST.get('rcode')
    cursor = connection.cursor()
    sql = "select pcode,nm from bas_pur where special LIKE '%2%' "
    cursor.execute(sql)
    # 供应商角色权限列表
    purList = cursor.fetchall()
    for d in purList:
        pur = {}
        pur['pcode'] = d[0]
        pur['nm'] = d[1]
        purL.append(pur)

    sql_UserPur = "select pcode from bas_role_pur where rcode = " + rcode
    cursor.execute(sql_UserPur)
    # 供应商已赋予的权限
    userPurList = cursor.fetchall()
    uPurL = [up[0] for up in userPurList]
    rs = {}
    rs["purL"] = purL
    rs["uPurL"] = uPurL

    return HttpResponse(json.dumps(rs))


@csrf_exempt
def savePur(request):
    checkedList = request.POST.getlist('pcode')

    rs = {}
    rcode = request.POST.get('rcode')
    try:
        cursor = connection.cursor()
        sql = "delete from bas_role_pur where rcode=" + rcode
        cursor.execute(sql)
        for row in checkedList:
            sql = "insert into bas_role_pur(rcode, pcode, pccode, status) values ('" + rcode + "','" + row + "', 0, 0)"
            cursor.execute(sql)
        rs["flag"] = '0'
    except Exception as e:
        print(e)
        rs["flag"] = '1'
    return HttpResponse(json.dumps(rs))
