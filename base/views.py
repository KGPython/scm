#-*- coding:utf-8 -*-

from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.template import loader,Context
from base.models import BasShop, SerialNumber, BasOrg, BasKe, BasGoods
from base.utils import MethodUtil

def global_setting(request):
    grpcode = request.session.get("s_grpcode")
    utype =  request.session.get("s_utype")
    if utype == "2":
        spercode = request.session.get("s_suppcode")
         # 商品小类信息
        deptList = BasGoods.objects.filter(grpcode=grpcode, venderid=spercode).values("deptid", "deptname").order_by("deptid").distinct()
    else:
        spercode = ""
        deptList = []

    # 门店信息
    shopList = BasShop.objects.all().values("shopcode", "shopnm").filter(grpcode=grpcode).exclude(shopcode__startswith="A").exclude(shopcode__startswith="F")
    # 门店信息（字典）
    shopDict = findShop()
    # 序列配置信息
    serialList = SerialNumber.objects.all().values("name", "serialid")
    # 商品类别组织结构信息
    orgList = BasOrg.objects.all().values("orgname", "orgcode")
    # 零售商管理员信息
    basKeList = BasKe.objects.all().values("kbcode", "kbname")
    # 单据类型
    billTypeDict = getBillTpye()
    adBillDict = {"0": u"调整单", "2430": u"库存进价调整单", "2446": u"批次数量更正单", "2460": u"批次库存转移单"}
    qrStatusDict = {"Y":"已确认","N":"未确认"}
    gqStateDict = {"Y":"已过期","N":"未过期"}

    #经营方式（结算方式）
    conn = MethodUtil.getMssqlConn()
    cur = conn.cursor()
    sqlPay = "select id,name from paytype"
    cur.execute(sqlPay)
    payTypeList = cur.fetchall()

    return locals()


# 查询门店信息存储为一个字典
def findShop(shopcode=None):
    q = Q()
    if shopcode:
        q.add(Q(shopcode=shopcode), Q.AND)
    q.add(Q(grpcode="00069"), Q.AND)

    shopList = BasShop.objects.values("shopcode", "shopnm").filter(q).exclude(shopcode__startswith="A").exclude(
        shopcode__startswith="F")
    shopDict = {}
    for shop in shopList:
        shopDict[shop["shopcode"]] = shop['shopnm'].strip()
    return shopDict
	
def getBillTpye(billtypeid=None):
    kwsrgs={}
    if billtypeid:
        kwsrgs.setdefault('serialid',billtypeid)
    billTpyeList = SerialNumber.objects.values("name","serialid").filter(**kwsrgs)
    billtypeDict = {}
    for billtype in billTpyeList:
        billtypeDict[str(billtype['serialid'])] = billtype['name'].strip()
    return billtypeDict

#供应商首页
def index(request):

    return HttpResponseRedirect("/scm/base/supp/home/")
