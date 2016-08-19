# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil, MethodUtil as mtu
from base.models import Kglistnoret, BasPurLog
from django.http import HttpResponse
import datetime, calendar, decimal
import xlwt3 as xlwt


@csrf_exempt
def index(request):
    yesterday = DateUtil.get_day_of_day(-1)

    rlist = Kglistnoret.objects.values("shopid", "sdate", "stime", "listno", "posid", "cashierid", "name", "payreson", "paytype", "payvalue", "cardno").filter(sdate=yesterday)

    formate_data(rlist)

    print(rlist)


def formate_data(rlist):
    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item,decimal.Decimal):
                rows[k] = "%0.2f" % float(item)
            if isinstance(item,datetime.datetime):
                rows[k] = item.strftime("%Y-%m-%d")
