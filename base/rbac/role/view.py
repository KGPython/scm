# -*-  coding:utf-8 -*-
from django.shortcuts import render
from base.models import RbacRole, RbacRoleInfo
from django.http import HttpResponse
import json
from .froms import *


def index(request):
    roles = RbacRole.objects.values('role_id','role_name','status').order_by('status')
    return render(request,'rbac/role/index.html',locals())

def create(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        role = RbacRole.objects.values('role_id','role_name','status').filter(role_id=id).first()

    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        status = request.POST.get('status')
        res = {}
        try:
            if id:
                role = RbacRole.objects.filter(role_id=id).update(role_name=name,status=status)
            else:
                role = RbacRole()
                role.role_name = name
                role.status = status
                role.save()
            res['msg'] = 0
        except Exception as e:
            print(e)
            res['msg'] = 1
    return render(request,'rbac/role/create.html',locals())

def delete(request):
    pass

def info(request):
    roleID = request.GET.get('id')
    #获取业态相关分类信息
    departs = getDeparts()
    #获取部类相关分类信息
    classes =  getClasses()
    # 获取功能模块相关分类信息
    modules = getModules()
    roleID = request.GET.get('id')
    role = RbacRoleInfo.objects.values('depart', 'category', 'module').filter(role_id=roleID).first()
    data = {}

    if role:
        departs = role['depart'].replace('},', '}$')
        departList = departs.split('$')
        for depart in departList:
            depart = json.loads(depart)
            if depart['p_id'] == '11':
                data['chaoShi'] = getFormData(depart['sub'])
            elif depart['p_id'] == '12':
                data['baiHuo'] = getFormData(depart['sub'])
            elif depart['p_id'] == '13':
                data['bianLiDian'] = getFormData(depart['sub'])

        categories = role['category'].replace('},', '}$')
        categoryList = categories.split('$')
        for category in categoryList:
            category = json.loads(category)
            if category['p_id'] == '1':
                data['shengXian'] = getFormData(category['sub'])
            elif category['p_id'] == '2':
                data['shiPin'] = getFormData(category['sub'])
            elif category['p_id'] == '3':
                data['feiShi'] = getFormData(category['sub'])
            elif category['p_id'] == '4':
                data['jiaDian'] = getFormData(category['sub'])
            elif category['p_id'] == '6':
                data['yunYing'] = getFormData(category['sub'])

        modules = role['module'].replace('},', '}$')
        moduleList = modules.split('$')
        for module in moduleList:
            module = json.loads(module)
            if module['p_id'] == '1':
                data['dailyCHSH'] = getFormData(module['sub'])
            elif module['p_id'] == '2':
                data['dailyBH'] = getFormData(module['sub'])
            elif module['p_id'] == '3':
                data['dailyBLD'] = getFormData(module['sub'])
            elif module['p_id'] == '4':
                data['dailyErr'] = getFormData(module['sub'])

    form = roleInfoForm(data)
    return render(request, 'rbac/role/roleInfo.html', locals())

def getFormData(subStr):
    subStr = subStr[0:len(subStr)-1]
    subList = subStr.split(',')
    data = set()
    for sub in subList:
        data.add(sub)
    return data

def infoSave(request):
    role_id = request.POST.get('id')
    departs = request.POST.get('departs')
    categories = request.POST.get('categories')
    modules = request.POST.get('modules')
    res = {}
    try:
        role = RbacRoleInfo()
        role.depart = departs
        role.category = categories
        role.module = modules
        role.role_id = role_id
        role.save()
        res['msg'] = 0
    except Exception as e:
        print(e)
        res['msg'] = 1

    return HttpResponse(json.dumps(res))

def getDeparts():
    companys = RbacShop.objects.values('shoptype').distinct()
    departs = RbacShop.objects.values('shopcode','shopnm','shoptype').filter(shoptype__in=(11,12,13),enable=1)
    data = []
    for company in companys:
        item = {}
        c_tpye = company['shoptype'].strip()
        item['p_item'] = {'c_id' : c_tpye}
        item['sub'] = []
        for depart in departs :
            if depart['shoptype'].strip() == c_tpye :
                item['sub'].append({'depart_id':depart['shopcode'],'depart_name':depart['shopnm']})
        data.append(item)
    return data

def getClasses():
    catrgories = BasOrg.objects.values('orgcode','orgname','parentcode').filter(tier=1,orgcode__in=(1,2,3,4,6))
    classes = BasOrg.objects.values('orgcode','orgname','parentcode').filter(tier=2)
    data = []
    for catrgory in catrgories:
        item = {}
        c_id = catrgory['orgcode']
        item['p_item'] = {'c_id':c_id,'c_name':catrgory['orgname']}
        item['sub'] = []
        for obj in classes:
            if obj['parentcode'] == c_id:
                item['sub'].append({'class_id':obj['orgcode'],'class_name':obj['orgname']})
        data.append(item)

    return data

def getModules():
    modules = RbacMoudle.objects.values('m_name','m_id').filter(status=1,p_id=0)
    modulesChild = RbacMoudle.objects.values('m_name','m_id','p_id').filter(status=1).exclude(p_id='')
    data = []
    for m in modules:
        item = {}
        p_id = m['m_id']
        item['p_item'] = {'m_id':p_id,'m_name':m['m_name']}
        item['sub'] = []
        for c in modulesChild:
            if c['p_id'] == p_id:
                item['sub'].append({'m_id':c['m_id'],'m_name':c['m_name']})
        data.append(item)
    return data