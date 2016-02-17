#-*- coding:utf-8 -*-

from django.shortcuts import render
from .forms import *
from base.models import BasRole,BasSuppLand,BasUserClass,BasRolePur
from django.core.paginator import Paginator
import time
from django.db import connection
from django.http import HttpResponseRedirect


nowTime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
def roleEdit(request):
    userType =  request.session.get('s_utype','1')

    rcode = request.GET.get('rcode','')     #右侧表单数据展示
    grpCode = request.GET.get('grpcode','00069')
    action = request.GET.get('action','')

    #分页相关
    page = int(request.GET.get('page',1))
    retRoleList = BasRole.objects.values('nm','rcode','remark','status','grpcode').filter(grpcode=grpCode)
    paginator = Paginator(retRoleList,20)
    try:
        retRoleList = paginator.page(page)
    except Exception as e:
        print(e)

    if request.method == 'POST':
        form = retRoleForm(request.POST)
        if action == 'save':
            if form.is_valid():
                nm = form.cleaned_data['nm']
                status = form.cleaned_data['status']
                grpCode = form.cleaned_data['grpcode']
                remark = form.cleaned_data['remark']

                if request.GET.get('recode'):       #编辑->保存
                    role = BasRole.objects.filter(rcode=rcode).update(nm=nm,status=status,grpcode=grpCode,remark=remark)

                else:       #新建->保存
                    rcode = form.cleaned_data['rcode']
                    role = BasRole()
                    role.nm = nm
                    role.rcode = rcode
                    role.status = status
                    role.grpcode = grpCode
                    role.remark = remark
                    role.save()
                    return HttpResponseRedirect('/scm/base/admin/retrole/edit/?rcode='+rcode+"&page="+str(page))

        elif action == 'del':       #删除角色
            if form.is_valid():
                rcode = form.cleaned_data['rcode']
                role = BasRole.objects.filter(rcode=rcode).delete()
                form = retRoleForm()

        elif action == 'new':       #新建角色
            form = retRoleForm()

        elif action == 'shopSave':          #门店设置
            if rcode:
                rolShopSel = request.POST.getlist('rolShop')
                BasUserClass.objects.filter(ucode=rcode,tablecode='roleshop').delete()
                for shopid in rolShopSel:
                    role =BasUserClass()
                    role.ucode =rcode
                    role.orgcode = shopid
                    role.tablecode = 'roleshop'
                    role.status = '0'
                    role.save()
                return HttpResponseRedirect('/scm/base/admin/retrole/edit/?rcode='+rcode+"&page="+str(page))
            else:
                errorMsg='请先创建角色，保存后，再设置门店，谢谢'

        elif action == 'powerSave':          #权限设置
            if rcode:
                rolPowerSel = request.POST.getlist('powerSel')
                BasRolePur.objects.filter(rcode=rcode).delete()
                for rolPower in rolPowerSel:
                    role = BasRolePur()
                    role.rcode = rcode
                    role.pcode = rolPower
                    role.pccode = '0'
                    role.status = 0
                    role.save()
                return HttpResponseRedirect('/scm/base/admin/retrole/edit/?rcode='+rcode+"&page="+str(page))
            else:
                errorMsg='请先创建角色，保存后，再设置权限，谢谢'
    else:       #右侧表单数据展示
        if rcode:       #点击左侧列表中的人员，右侧展示详细信息
            role = BasRole.objects.values('nm','rcode','remark','status','grpcode').get(rcode=rcode)
            form = retRoleForm(role)

            #权限列表
            #update start by liubf at 2016/01/25
            # grpCode = role['grpcode']
            # sqlWhere = ''
            # if len(grpCode)==1:
            #     if grpCode == 3:
            #         grpCode = 2
            #         sqlWhere = "b.special like '%"+grpCode+"%'"
            # else:
            #   sqlWhere = "b.special like '%"+userType+"%'"

            sql = "SELECT DISTINCT pcode,nm FROM bas_pur  WHERE special like '%"+userType+"%' ORDER BY pcode"
            #update end by liubf at 2016/01/25
            cursor = connection.cursor()
            cursor.execute(sql)
            rolPowerList = cursor.fetchall()
            cursor.close()
            connection.close()

            sql = "select pcode from bas_role_pur where rcode ='"+rcode+"' order by pcode"
            cursor = connection.cursor()
            cursor.execute(sql)
            rolPowerLoad = cursor.fetchall()
            print(rolPowerLoad)
            cursor.close()
            connection.close()


            #门店列表
            rolShopLoad = BasUserClass.objects.values('orgcode').filter(ucode=rcode,tablecode='roleshop')
        else:
            form = retRoleForm()
    return render(request,'admin/sysConf_retail.html',locals())


def log(request):
    supName = ''
    suppCode = ''
    start = ''
    end = ''
    page = request.GET.get('page',1)
    if request.method == 'POST':
        form = logForm(request.POST)
        if form.is_valid():
            suppCode = form.cleaned_data['suppcode']
            supName = form.cleaned_data['supname']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
    else:
        suppCode = request.GET.get('suppcode','')
        supName = request.GET.get('supname','')
        start = request.GET.get('start',nowTime)
        end = request.GET.get('end',nowTime)
        data={'suppcode':suppCode,'supname':supName,'start':start,'end':end}
        form = logForm(data)

    kwarg={}
    if suppCode:
        kwarg.setdefault('suppcode',suppCode)
    if supName:
        kwarg.setdefault('supname',supName)
    kwarg.setdefault('lastlandtime__gte',start)
    kwarg.setdefault('lastlandtime__lte',"{end} 23:59:59".format(end=end))

    retlandList = BasSuppLand.objects.values('suppcode','supname','lastlandtime','status','landcs')\
                                     .filter(**kwarg).order_by('-lastlandtime')
    paginator = Paginator(retlandList,10)
    try:
        retlandList = paginator.page(page)
    except Exception as e:
        print(e)
    return render(request,
                  'admin/sysConf_retail_log.html',
                  {
                      'form':form,
                      'suppCode':suppCode,
                      'supName':supName,
                      'start':str(start),
                      'end':str(end),
                      'retlandList':retlandList,
                      'page':page
                  })