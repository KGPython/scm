#-*- coding:utf-8 -*-
__author__ = "liubf"

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from base.supplier.forms import ChangepwdForm
from base.utils import MethodUtil as mtu
from base.message.views import findPubInfoAllByCon
from base.models import ReconcilItem,Reconcil,BasFee
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
    ritem = ReconcilItem.objects.filter(pid=paytypeid).values("rid")
    if ritem:
        rid = ritem[0]["rid"]
        reconcil = Reconcil.objects.filter(id=rid,status=1).values("rname","beginday","endday")
        rdays =[]
        tdays = []
        for row in reconcil:
            begin = row["beginday"]
            end = row["endday"]
            rdays.append("{begin}-{end}".format(begin=begin,end=end))
            if begin<=15:
                tdays.append("1-{begin}".format(begin=begin))
            else:
                tdays.append("15-{begin}".format(begin=begin))

        rds = ",".join(rdays)
        tds = ",".join(tdays)

    fee = BasFee.objects.get(suppcode=suppcode,grpcode=s_grpcode,ucode=user["ucode"])
    endDate = fee.enddate

    conn = mtu.get_MssqlConn()
    #g-购销 l-联营 d-代销  z-租赁
    pstart,pend,cstart,cend = getStartAndEndDate(contracttype)
    #查询单据信息（动态查询）
    rdict = findBillItem(conn,suppcode,pstart,pend,cstart,cend,None,contracttype)
    if rdict and  rdict["blist"]:
        blist = rdict["blist"]
        blen = len(blist)
        request.session["s_rdict"] = blen
    else:
        request.session["s_rdict"] = 0
    conn.close()

    return render(request,"index.html",{"page":page,"pageNum":pageNum,"pwdInit":pwdInit,"rdays":rds,"tdays":tds,"endDate":endDate})

#供应商修改密码
@csrf_exempt
def repwd(request):
    form = ChangepwdForm()
    return render(request,"user_setpwd.html",locals())


