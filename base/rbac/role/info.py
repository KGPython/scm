# -*-  coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json
from base.models import RbacShop,BasOrg,RbacRoleInfo,RbacUserRole,RbacMoudle


def index(request):
    #获取业态相关分类信息
    departs = getDeparts()
    #获取部类相关分类信息
    classes =  getClasses()
    # 获取功能模块相关分类信息
    modules = getModules()

    return render(request, 'rbac/role/role.html', locals())

def save(request):
    role_id = '0001'
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
        res['status'] = 'ok'
    except Exception as e:
        print(e)
        res['status'] = 'fail'

    return HttpResponse(json.dumps(res))

def show(request):
    u_id = request.session.get('s_ucode')
    role_id = RbacUserRole.objects.values('role').filter(user_id=u_id)
    role = RbacRoleInfo.objects.values('depart','category','module').filter(role_id=role_id)[0]
    request.session['rbac_role'] = role
    #业态
    departStr = role['depart'].replace('},', '}$')
    departList = departStr.split('$')
    companyIdList = []
    for depart in departList:
        depart = json.loads(depart)
        companyIdList.append(depart['p_id'])
    #部类
    categoryStr = role['category'].replace('},', '}$')
    categoryList = categoryStr.split('$')
    #模块
    moduleStr = role['module'].replace('},', '}$')
    moduleList = moduleStr.split('$',)
    moduleIdList = []
    for module in moduleList:
        module = json.loads(module)
        moduleIdList.append(module['p_id'])
        subModules = module['sub'][0:len(module['sub'])-1].split(',')
        moduleIdList = moduleIdList+subModules

    navList = RbacMoudle.objects.values('m_name','m_id','m_url','p_id').filter(m_type__in=companyIdList,m_id__in=moduleIdList)
    #用companyList
    print(navList)





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


