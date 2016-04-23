#-*- coding:utf-8 -*-
__author__ = "liubf"

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from base.supplier.forms import ChangepwdForm
from base.utils import MethodUtil as mtu
from base.message.views import findPubInfoAllByCon
from base.models import ReconcilItem,Reconcil,BasFee,BasPayType
from base.supplier.balance.views import getStartAndEndDate,findBillItem

from django.core.paginator import Paginator

__EACH_PAGE_SHOW_NUMBER = 10

# Create your views here.

#供应商主页
@csrf_exempt
def index(request):

    user = request.session.get("s_user",None)
    suppcode = request.session.get("s_suppcode")
    s_grpcode = request.session.get("s_grpcode")
    paytypeid = request.session.get("s_paytypeid")
    contracttype = request.session.get("s_contracttype")
    if user:
        pubList = findPubInfoAllByCon(user)
    else:
        pubList = []

    pageNum = int(request.GET.get("pageNum",1))

    page =  Paginator(pubList,__EACH_PAGE_SHOW_NUMBER,allow_empty_first_page=True).page(pageNum)

    upwd = user["password"]
    pwd = mtu.md5(suppcode)
    pwdInit = False
    if upwd == pwd:
        pwdInit = True

    #查询对账日期
    ritemList = ReconcilItem.objects.filter(pid=paytypeid).values("rid")
    rdays =[]
    tdays = []
    rlist = []
    if ritemList:
        for ritem in ritemList:
            rid = ritem["rid"]
            reconcil = Reconcil.objects.filter(id=rid,status=1).values("rname","beginday","endday")
            if reconcil:
                row = reconcil[0]
                rlist.append(dict(row))

    rlist = sorted(rlist,key=lambda row: row["beginday"])
    rds = ""
    tds = ""
    if rlist:
        for rw in rlist:
            begin = rw["beginday"]
            end = rw["endday"]

            rdays.append("{begin}-{end}".format(begin=begin,end=end))
            if "随时" in rw["rname"]:
                 tdays.append("{begin}-{end}".format(begin=begin,end=end))
            else:
                if begin<=15:
                    tdays.append("1-{begin}".format(begin=begin-1))
                else:
                    tdays.append("16-{begin}".format(begin=begin-1))
        rds = ",".join(rdays)
        tds = ",".join(tdays)

    endDate = ""
    try:
        fee = BasFee.objects.get(suppcode=suppcode,grpcode=s_grpcode,ucode=user["ucode"])
        if fee:
            endDate = fee.enddate

        conn = mtu.get_MssqlConn()
         #供应商结算方式
        pdict = findPayType(2)
        if pdict and paytypeid:
            payTypeName = pdict[str(int(paytypeid))]
        else:
            payTypeName = ""
        #g-购销 l-联营 d-代销  z-租赁
        pstart,pend,cstart,cend = getStartAndEndDate(contracttype,payTypeName)
        #查询单据信息（动态查询）
        rdict = findBillItem(conn,suppcode,pstart,pend,cstart,cend,None,contracttype)
        if rdict and rdict["blist"]:
            blist = rdict["blist"]
            blen = len(blist)
            request.session["s_rdict"] = blen
        else:
            request.session["s_rdict"] = 0
        conn.close()
    except Exception as e:
        print(e)

    return render(request,"index.html",{"page":page,"pageNum":pageNum,"pwdInit":pwdInit,"rdays":rds,"tdays":tds,"endDate":endDate,"payTypeName":payTypeName})

def findPayType(type):
    payTypeList = BasPayType.objects.all().values("id","name")
    if type==1:
        return payTypeList
    else:
        pdict = {str(int(row["id"])):row["name"] for row in payTypeList}
        return pdict
#供应商修改密码
@csrf_exempt
def repwd(request):
    form = ChangepwdForm()
    return render(request,"user_setpwd.html",locals())


