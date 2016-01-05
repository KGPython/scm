#-*- coding:utf-8 -*-
__author__ = "liubf"

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from base.supplier.forms import ChangepwdForm
from base.utils import MethodUtil as mtu
from base.message.views import findPubInfoAllByCon


from django.core.paginator import Paginator

__EACH_PAGE_SHOW_NUMBER = 10

# Create your views here.

#供应商主页
@csrf_exempt
def index(request):

     user = request.session.get("s_user",None)
     suppcode = request.session.get("s_suppcode")
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

     return render(request,"index.html",{"page":page,"pageNum":pageNum,"pwdInit":pwdInit})


#供应商修改密码
@csrf_exempt
def repwd(request):
    form = ChangepwdForm()
    return render(request,"user_setpwd.html",locals())


