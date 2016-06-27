#-*- coding:utf-8 -*-
__author__ = 'liubf'

import json,datetime
from io import BytesIO

from django.db import connection
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator

from base.message.views import findPubInfoAllByCon
from base.utils import MethodUtil as mtu,Constants
from base.models import BasUser,BasUserRole,BasSupplier,BasGroup,BasFee,BasRole,BasSuppLand

__EACH_PAGE_SHOW_NUMBER = 10

#供应商首页
# def index(request):
#
#     return HttpResponseRedirect("/scm/base/supp/home/")

def loginPage(request):

    return render(request, "login.html")

#登录
@csrf_exempt
def login(request):
    ucode = mtu.getReqVal(request,"ucode","")
    password = mtu.getReqVal(request,"password","")
    vcode = mtu.getReqVal(request,"vcode","")
    try:
        olduser = request.session.get("s_user",default=None)
        vcode2 = request.session["s_vcode"]
    except:
        olduser = []
        vcode2 = ""

    response_data = {}
    try:
        #判断是否过期：过期后不显示业务菜单，只显示首页、退出，提醒已经过期。
        if not olduser:
            if vcode==vcode2:
                #查询用户信息
                user = BasUser.objects.get(ucode=ucode)

                if user:
                    upwd = user.password
                    password = mtu.md5(password)
                    if upwd==password:
                        request.session["s_user"] = user.toDict()
                        request.session["s_ucode"] = user.ucode
                        request.session["s_uname"] = user.nm
                        request.session["s_utype"] = user.utype
                        request.session["menu_type"] = user.utype
                        #根据grpcode查询grpname：
                        #   如果utype==2，登录用户为供应商则grpname为供应商名称
                        #   如果utype==1，登录用户为零售商则grpname为零售商名称
                        if user.utype == "2":    #供应商
                            grpcode = findGrpCodeBySuppCode(user.grpcode)
                            request.session["s_grpcode"] = grpcode
                            try:
                                fee =  BasFee.objects.get(suppcode=user.grpcode,grpcode=grpcode,ucode=ucode)
                                request.session["s_fee"] = fee.toDict()
                            except Exception as e:
                                print(e)
                                request.session["s_fee"] = {"status":"N"}
                            request.session["s_suppcode"] = user.grpcode

                            supp = findGrpNameByCode(user.grpcode,user.utype)
                            request.session["s_suppname"] = supp.chnm
                            request.session["s_contracttype"] = supp.contracttype
                            request.session["s_paytypeid"] = supp.paytypeid
                            request.session["s_bank"] = supp.bank
                            request.session["s_accountno"] = supp.accountno

                            grp = findGrpNameByCode(grpcode,"1")
                            request.session["s_grpname"] = grp.grpnm

                            response_data['homeurl'] = Constants.URL_SUPPLIER_HOME

                        else:    #零售商
                            request.session["s_grpcode"] = user.grpcode

                            grp = findGrpNameByCode(user.grpcode,user.utype)
                            request.session["s_grpname"] = grp.grpnm
                            request.session["s_fee"] = {}
                            response_data['homeurl'] = Constants.URL_RETAILER_HOME

                        request.session["homeurl"] = response_data['homeurl']
                        #查询角色，多个角色用“，”分割
                        urs = findRoleByUcode(user.ucode)
                        if urs:
                            urole = urs[0]
                            #查询菜单权限
                            purlist = findPurByRcode(urs[2])
                            request.session["s_rcodes"] = urs[1]
                            request.session["isadmin"] = urs[3]
                            request.session["s_urole"] = urole
                            request.session["s_umenu"] = getMenu(purlist)
                            response_data['status'] = "0"

                            #添加登录日志
                            if user.utype=="2":
                                lastlandtime = datetime.date.today().strftime("%Y-%m-%d")
                                slist = BasSuppLand.objects.filter(suppcode=user.grpcode,lastlandtime__gte="{lastlandtime} 00:00:00".format(lastlandtime=lastlandtime)).values("landcs")
                                if slist and slist[0]:
                                    sland = slist[0]
                                    landcs=sland["landcs"]+1
                                    BasSuppLand.objects.filter(suppcode=user.grpcode,lastlandtime__gte="{lastlandtime} 00:00:00".format(lastlandtime=lastlandtime)).update(landcs=landcs,lastlandtime=datetime.datetime.today())
                                else:
                                    fee =  request.session.get("s_fee")
                                    if fee:
                                        status = fee["status"]
                                    else:
                                        status = "N"
                                    suppname =  request.session.get("s_suppname")
                                    lastLand = BasSuppLand.objects.values("allcs").latest("allcs")
                                    if lastLand:
                                        allcs = lastLand["allcs"]+1
                                    else:
                                        allcs = 1

                                    bs =  BasSuppLand()
                                    bs.grpcode = "00069"
                                    bs.utype = "2"
                                    bs.suppcode = user.grpcode
                                    bs.landcs = 1
                                    bs.lastlandtime = datetime.date.today()
                                    bs.status = status
                                    bs.supname = suppname
                                    bs.remark=""
                                    bs.ylzd1=""
                                    bs.ylzd2=""
                                    bs.allcs= allcs
                                    bs.save()

                        else:
                            response_data['status'] = "4"
                    else:
                        response_data['status'] = "2"
                else:
                    response_data['status'] = "1"
            else:
                response_data['status'] = "3"
        else:
            response_data['status'] = "0"
            if olduser["utype"] == "1":
                response_data['homeurl'] = Constants.URL_RETAILER_HOME
            else:
                response_data['homeurl'] = Constants.URL_SUPPLIER_HOME
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def menu(request):
    mtype = mtu.getReqVal(request,"mtype","1")
    request.session["menu_type"] = mtype

    user = request.session.get("s_user",None)
    if user:
         pubList = findPubInfoAllByCon(user)
    else:
         pubList = []

    pageNum = int(request.GET.get("pageNum",1))

    page =  Paginator(pubList,__EACH_PAGE_SHOW_NUMBER,allow_empty_first_page=True).page(pageNum)

    return render(request,"admin/index.html",{"page":page,"pageNum":pageNum})

def getCodeByName(name):
    if name == "供应商":
        return "supplier"
    elif name=="零售商":
        return "retailer"
    else:
        return "system"


#菜单分组
def getMenu(purlist):
    rlist = []
    m1list = []
    for row in purlist:
        grpname = getCodeByName(row["grpname"].strip())
        rlist.append(grpname)
        m1list.append((row["parentnm"].strip(),grpname))

    #去重
    rlist = list(set(rlist))
    m1list = list(set(m1list))
    #排序
    m1list = sorted(m1list, key=lambda menu: menu[0])

    dt = {}
    pinyin = mtu.PinYin()
    for r in rlist:
        mls = []
        for m in m1list:
            if r==m[1]:
                dls = []
                for d in purlist:
                    if m[0]==d['parentnm'].strip():
                        dls.append(d)
                mkey = cutStr(m[0],".")
                mls.append([m[0],dls,pinyin.hanzi2pinyin_split(string=mkey, split="")])
        dt[r] = mls

    #print(">>>>>>菜单：",dt)
    return dt

def cutStr(str,separator):
    try:
        index = str.index(separator)
        return str[index+1:]
    except:
        return str

#根据供应商编码查询供应商所属单位编码
def findGrpCodeBySuppCode(suppcode):
    obj = BasFee.objects.filter(suppcode=suppcode,grpcode__isnull=False).values("grpcode").distinct()
    if obj:
        return obj[0]["grpcode"]
    else:
        return ""

#根据角色编码查询菜单
def findPurByRcode(rcodes):

    # sql = "select DISTINCT rp.pccode,rp.pcode,rp.status, "
    # sql += "p.nm,p.bmoudule,p.parent_nm,p.grpname,pc.spec "
    # sql += "from bas_role_pur rp,bas_pur p,bas_pchild pc "
    # sql += "where rp.pcode=p.pcode and rp.pccode=pc.pccode "
    # sql += "and rp.pcode<>'001' and p.status=1 "
    # if rcodes:
    #     sql += "and rp.rcode in ("+rcodes+") "
    #
    # sql += "order by p.parent_nm,p.pcode"

    sql = "select DISTINCT rp.pccode,rp.pcode,rp.status, "
    sql += "p.nm,p.bmoudule,p.parent_nm,p.grpname "
    sql += "from bas_role_pur rp,bas_pur p "
    sql += "where rp.pcode=p.pcode "
    sql += "and rp.pcode<>'001' and p.status=1 "
    if rcodes:
        sql += "and rp.rcode in (" + rcodes + ") "

    sql += "order by p.parent_nm,p.pcode"

    cursor = connection.cursor()
    cursor.execute(sql)
    plist = cursor.fetchall()
    rslist = []
    if plist:
        for p in plist:
            item = []
            item.append(("pccode",p[0]))
            item.append(("pcode",p[1]))
            item.append(("status",p[2]))
            item.append(("nm",p[3]))
            item.append(("bmoudule",p[4]))
            item.append(("parentnm",p[5]))
            item.append(("grpname",p[6]))
            # item.append(("spec",p[7]))
            rslist.append(dict(item))
    return rslist

#根据用户编码查询用户所属角色
def findRoleByUcode(ucode):

    rcodes = BasUserRole.objects.filter(ucode=ucode).values("rcode")
    clist = []
    if rcodes:
        clist = [code['rcode'] for code in rcodes]

    codes = "'"+"','".join(clist)+"'"

    roles = BasRole.objects.filter(rcode__in=clist).values("rcode","nm","remark","status","grpcode")
    rolelist = list(roles)
    if not roles:
        rolelist = []

    #判断是否为超级管理员
    try:
        clist.index("1")
        isadmin = 1
    except:
        isadmin = -1

    return [rolelist,clist,codes,isadmin]

#根据供应商编码或供应商所属单位编码查询单位名称
def findGrpNameByCode(grpcode,utype):
    if utype == '2':
        obj =  BasSupplier.objects.get(suppcode=grpcode)
    else:
        obj = BasGroup.objects.get(grpcode=grpcode)

    return obj

#验证码
def vcode(request):
    image = mtu.verifycode(request,'s_vcode')
    #将image信息保存到BytesIO流中
    buff = BytesIO()
    image.save(buff,"png")
    return HttpResponse(buff.getvalue(),'image/png')

#注销
def logout(request):
    try:
        del request.session["s_user"]
        del request.session["s_ucode"]
        del request.session["s_uname"]
        del request.session["s_urole"]
        del request.session["s_umenu"]
        del request.session["s_grpcode"]
        del request.session["s_grpname"]
        del request.session["s_utype"]
        del request.session["s_suppcode"]
        del request.session["s_suppname"]
        del request.session["s_contracttype"]
        del request.session["s_paytypeid"]
    except:
        print("session[s_user]不存在")

    return render(request,"login.html")

@csrf_exempt
def uppwd(request):
    data = {}
    flag = mtu.getReqVal(request,"flag")
    #修改
    if flag=="1":
        user = request.session.get("s_user",None)
        ucode = user["ucode"]
    elif flag=="2":
        ucode = mtu.getReqVal(request,"ucode")

    data["result"] = "1"
    try:
        newPwd = mtu.getReqVal(request,"newPwd","")
        pwd = mtu.md5(newPwd)
        BasUser.objects.filter(ucode=ucode).update(password=pwd)

        data["result"] = "0"
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(data))


# 欢迎
def welcome(request):
    return render(request,'welcome.html')


