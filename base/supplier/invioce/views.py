__author__ = 'Administrator'
from base.utils import MethodUtil
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def createInvioce(request):
    return render(request,'user_invoice.html',locals())

@csrf_exempt
def saveInvioce(request):
    jsonStr = request.POST.get('jsonStr','')
    print(jsonStr)
    conn = MethodUtil.getMssqlConn()
    sql = ''
    cur = conn.cursor()
    cur.execute(sql)
    return HttpResponse()
