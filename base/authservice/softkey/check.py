__author__ = 'admin'
import random,json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import hashlib
from base.utils import MethodUtil as mth

@csrf_exempt
def index(request):
    call = request.POST.get('call')
    if call == '100':
        number1 = random.randint(1,65536)
        number2 = random.randint(1,65536)
        randNum = str(number1)+str(number2)
        dt = datetime.datetime.now() + datetime.timedelta(hours=int(1))
        res = {}
        res['randNum'] = randNum
        response = HttpResponse(json.dumps(res))
        response.set_cookie("randNum",randNum,expires=dt)
    else:
        signClient = request.POST.get('signClient')

        randNum = request.COOKIES["randNum"]
        keyId = request.POST.get('keyId')
        timeStr = request.POST.get('time')

        conn = mth.getSoftKeySql()
        sql = 'SELECT username,status FROM bas_softkey WHERE KeyID = "{keyId}"'.format(keyId=keyId)
        cur = conn.cursor()
        cur.execute(sql)
        softKey = cur.fetchone()
        userName = (softKey['username']).encode(encoding='UTF-8')
        m = hashlib.md5()
        m.update(userName)
        userName = m.hexdigest()

        signList = [keyId,userName,randNum,timeStr]
        signList.sort()
        signStr = ''.join(signList)
        signStr = signStr.encode(encoding='UTF-8')
        signServer = hashlib.sha1(signStr).hexdigest()

        res = {}
        if signClient == signServer:
            res['msg'] = softKey['status']

        response = HttpResponse(json.dumps(res))

    return response