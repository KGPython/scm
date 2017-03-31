#-*- coding:utf-8 -*-

from django.db.models import Q
from django.http import HttpResponseRedirect
from base.models import BasShop, SerialNumber, BasOrg, BasKe, BasGoods,BasPayType
from base.utils import Constants

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
    orgDict = {row["orgcode"]:row["orgname"] for row in orgList}
    # 零售商管理员信息
    basKeList = BasKe.objects.all().values("kbcode", "kbname")
    # 单据类型
    billTypeDict = getBillTpye()
    adBillDict = {"0": u"调整单", "2430": u"库存进价调整单", "2446": u"批次数量更正单", "2460": u"批次库存转移单"}
    qrStatusDict = {"Y":"已确认","N":"未确认"}
    gqStateDict = {"Y":"已过期","N":"未过期"}
    kxTypeDict = {"0":"固定","1":"临时"}
    kkflagDict = {"0":"交款","1":"扣款"}
    prtflagDict = {"0":"不冲","1":"冲"}

    countMethodDict = {"0":"按结算单收取","1":"按月收取","2":"按年收取"}
    userStatus = Constants.USER_STATUS
    #经营方式
    contractTypeDict = Constants.CONTRACT_TYPE_DICT
    #结算方式
    payTypeList = findPayType(1)
    payTypeDict = findPayType(2)

    # 加密狗验证服务地址
    SCM_SOFTKEY_URL = "http://192.168.250.8:8082/authservice/inf/main"
    # SCM_SOFTKEY_URL = "http://192.168.122.120:8080/authservice/inf/main"   #本地测试地址
    return locals()


def findPayType(type):
    payTypeList = BasPayType.objects.all().values("id","name")
    if type==1:
        return payTypeList
    else:
        pdict = {str(int(row["id"])):row["name"] for row in payTypeList}
        return pdict

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
