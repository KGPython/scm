#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.shortcuts import render
from base.utils import MethodUtil as mtu,DateUtil
from base.models import BasPurLog
import datetime;

__EACH_PAGE_SHOW_NUMBER = 10

@csrf_exempt
def purlog(request):
    pageNum = mtu.getReqVal(request,"pageNum","1")
    start = mtu.getReqVal(request,"start")
    end = mtu.getReqVal(request,"end")
    ucode = mtu.getReqVal(request,"ucode","")
    pname = mtu.getReqVal(request,"pname","")

    try:
        karrs = {}
        if not start:
            start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
        if not end:
            end = datetime.datetime.today().strftime("%Y-%m-%d")

        karrs.setdefault("createtime__gte", "{start} 00:00:00".format(start=start))
        karrs.setdefault("createtime__lte", "{end} 23:59:59".format(end=end))
        karrs.setdefault("ucode__contains", "{ucode}".format(ucode=ucode))
        karrs.setdefault("name__contains", "{pname}".format(pname=pname))

        rlist = BasPurLog.objects.all().filter(**karrs).order_by("-createtime")
    except Exception as e:
        rlist = []
        print(e)

    page = Paginator(rlist, __EACH_PAGE_SHOW_NUMBER, allow_empty_first_page=True).page(int(pageNum))
    result = {"page": page, "pageNum": str(pageNum), "start": start,"end":end,"ucode":ucode,"pname":pname,"qtype_dict":{"1":"查询","2":"下载"}}
    return render(request, "admin/sysConf_retail_purlog.html", result)

def report(request):
    pageNum = mtu.getReqVal(request, "pageNum", "1")
    start = mtu.getReqVal(request, "start")
    end = mtu.getReqVal(request, "end")
    ucode = mtu.getReqVal(request, "ucode", "")
    pname = mtu.getReqVal(request, "pname", "")
    try:
        if not start:
            start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
        if not end:
            end = datetime.datetime.today().strftime("%Y-%m-%d")

        conn = mtu.getMysqlConn()
        cur = conn.cursor()

        condition = " where 1=1 "
        condition += " and createtime BETWEEN '{start} 00:00:00' AND '{end} 23:59:59'"\
                     .format(start=start,end=end)
        if ucode:
             condition += " and ucode like '%{ucode}%'".format(ucode=ucode)
        if pname:
            condition += " and name like '%{pname}%'".format(pname=pname)

        sql = "SELECT DATE_FORMAT(createtime,'%Y-%m-%d') createtime,`name`,url," \
              "SUM(CASE WHEN qtype = 1 THEN 1 ELSE 0 END) views," \
              "SUM(CASE WHEN qtype = 2 THEN 1 ELSE 0 END) downs " \
              "FROM bas_pur_log {condition} GROUP BY DATE_FORMAT(createtime,'%Y-%m-%d'),`name` "\
              "order by DATE_FORMAT(createtime,'%Y-%m-%d') DESC "\
              .format(condition=condition)

        cur.execute(sql)
        rlist = cur.fetchall()
        mtu.close(conn,cur)
    except Exception as e:
        rlist = []
        print(e)

    page = Paginator(rlist, __EACH_PAGE_SHOW_NUMBER, allow_empty_first_page=True).page(int(pageNum))
    result = {"page": page, "pageNum": str(pageNum),"start": start,"end":end,"ucode":ucode,"pname":pname,}
    return render(request, "admin/sysConf_retail_purlog_report.html", result)
