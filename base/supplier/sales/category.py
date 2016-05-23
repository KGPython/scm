#-*- coding:utf-8 -*-
__author__ = 'liubf'

import datetime,decimal,time
import xlrd,xlwt3 as xlwt

from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from base.views import findShop
from base.utils import MethodUtil as mtu

@csrf_exempt
def query(request):
    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname","")

    shopcode = mtu.getReqVal(request,"shopCode","")
    sccode = mtu.getReqVal(request,"sccode","")
    start = mtu.getReqVal(request,"start","")
    end = mtu.getReqVal(request,"end","")
    qtype = mtu.getReqVal(request,"qtype","1")

     #当月1号
    if not start:
        start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    #当日
    if not end:
        end = datetime.datetime.today().strftime("%Y-%m-%d")

    codes = ''
    shops = ''
    shopDict = findShop()
    if shopcode:
        list = shopcode.split(",")
        for i in range(0,len(list)):
            code = list[i]
            if code:
                codes += " shopcode='%s' or" % code
                shops += "%s," % shopDict[str(code)]
        if codes:
            codes = codes[0:len(codes)-2]
            shops = shops[0:len(shops)-1]
    else:
        codes = '1=1'
        shops = '全部'

    ccodes = ''
    if sccode:
        list = sccode.split(",")
        for i in range(0,len(list)):
            code = list[i]
            if code:
                ccodes += " sccode like '"+code+"%' or"
        if ccodes:
            ccodes = ccodes[0:len(ccodes)-2]
    else:
        ccodes = '1=1'

    sum = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    sum4 = decimal.Decimal('0.0')
    try:
        sql1 = "select sum(scost) from sales_pro where grpcode='"+grpcode+"' "
        sql1 += "and supercode='"+spercode+"' and ("+codes+") and sstyle<>'' and "
        sql1 += "date_format(sdate,'%Y-%m-%d')>='"+start+"' and date_format(sdate,'%Y-%m-%d')<='"+end+"' and ("+ccodes+") "

        cursor = connection.cursor()
        cursor.execute(sql1)
        rsobj = cursor.fetchone()

        if rsobj:
            sum = rsobj[0]

        sql2 = "select tb1.sccode,tb1.scname,sum(tb1.num) as num,sum(tb1.svalue) as svalue,sum(tb1.discount) as discount,sum(tb1.scost) as scost "
        sql2 += " from( "
        sql2 += "     select sccode,scname,svalue,discount,scost,num from sales_pro "
        sql2 += "	  where grpcode='"+grpcode+"' "
        sql2 += "    and supercode='"+spercode+"' and ("+codes+") and sstyle<>'' and "
        sql2 += "    date_format(sdate,'%Y-%m-%d')>='"+start+"' and date_format(sdate,'%Y-%m-%d')<='"+end+"' and ("+ccodes+")  "
        sql2 += " ) tb1 "
        sql2 += "group by tb1.sccode,tb1.scname order by tb1.sccode "

        cursor.execute(sql2)
        list = cursor.fetchall()

        rslist = []
        if list:
            for row in list:

                item = ["","","","","","",""]
                item[0] = row[0]
                item[1] = row[1]
                item[2] = row[2]
                item[3] = (row[3]-row[4])
                item[4] = row[5]

                if sum:
                    radio = (row[5] / sum * 100)   #占比
                    sum4 += radio  #累计占比

                item[5] = radio
                item[6] = sum4

                sum1 += item[2]
                sum2 += item[3]
                sum3 += item[4]

                rslist.append(item)

        cursor.close()
    except Exception as e:
        print(e)

    if qtype=='1':
        result = {"rslist":rslist}
        result.setdefault("shops",shops)
        result.setdefault("grpcode",grpcode)
        result.setdefault("grpname",grpname)
        result.setdefault("shopCode",shopcode)
        result.setdefault("sccode",sccode)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))

        return render(request, "user_sale_ctg.html",result)
    else:
        return export(rslist,sum1,sum2,sum3)

#导出Excel
def export(rslist,sum1,sum2,sum3):
    sname = "类别销售汇总"

    titles = [("小类编码","1000"),("小类名称","1000"),("销售数量","1000"),("实际销售","1000"),
              ("销售成本","1000"),("占比(%)","500"),("累计占比(%)","1000")]

    sumlist = ["合计","",sum1,sum2,sum3,"100.00","100.0"]
    fmtlist = [None,None,"0.00","0.000","0.000","0.00","0.0"]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "sale_category.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

@csrf_exempt
def detail(request):
    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname","")
    shopcode = mtu.getReqVal(request,"shopCode","")
    sccode = mtu.getReqVal(request,"sccode","")
    start = mtu.getReqVal(request,"start","")
    end = mtu.getReqVal(request,"end","")
    qtype = mtu.getReqVal(request,"qtype","1")

     #当月1号
    if not start:
        start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    #当日
    if not end:
        end = datetime.datetime.today().strftime("%Y-%m-%d")

    codes = ''
    shops = ''
    shopDict = findShop()
    if shopcode:
        list = shopcode.split(",")
        for i in range(0,len(list)):
            code = list[i]
            if code:
                codes += " shopcode='%s' or" % code
                shops += "%s," % shopDict[str(code)]
        if codes:
            codes = codes[0:len(codes)-2]
            shops = shops[0:len(shops)-1]
    else:
        codes = '1=1'
        shops = '全部'

    ccodes = ''
    if sccode:
        list = sccode.split(",")
        for i in range(0,len(list)):
            code = list[i]
            if code:
                ccodes += " sccode like '"+code+"%' or"
        if ccodes:
            ccodes = ccodes[0:len(ccodes)-2]
    else:
        ccodes = '1=1'

    sum = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    sum4 = decimal.Decimal('0.0')
    try:
        sql1 = "select sum(scost) from sales_pro where grpcode='"+grpcode+"' "
        sql1 += "and supercode='"+spercode+"' and ("+codes+") and sstyle<>'' and "
        sql1 += "date_format(sdate,'%Y-%m-%d')>='"+start+"' and date_format(sdate,'%Y-%m-%d')<='"+end+"' and ("+ccodes+") "

        cursor = connection.cursor()
        cursor.execute(sql1)
        rsobj = cursor.fetchone()

        if rsobj:
            sum = rsobj[0]

        sql2 = "select tb1.sccode,tb1.scname,sum(tb1.num) as num,sum(tb1.svalue) as svalue,sum(tb1.discount) as discount,sum(tb1.scost) as scost "
        sql2 += ",tb1.sdate from( "
        sql2 += "     select sdate,sccode,scname,svalue,discount,scost,num from sales_pro "
        sql2 += "	  where grpcode='"+grpcode+"' "
        sql2 += "    and supercode='"+spercode+"' and ("+codes+") and sstyle<>'' and "
        sql2 += "    date_format(sdate,'%Y-%m-%d')>='"+start+"' and date_format(sdate,'%Y-%m-%d')<='"+end+"' and ("+ccodes+")  "
        sql2 += " ) tb1 "
        sql2 += "group by tb1.sccode,tb1.scname,tb1.sdate order by tb1.sccode "

        cursor.execute(sql2)
        list = cursor.fetchall()

        rslist = []
        if list:
            for row in list:
                item = ["","","","","","","",""]

                if sum:
                    radio = (row[5] / sum * 100)  #占比
                    sum4 += radio #累计占比

                item[0] = row[6]
                item[1] = row[0]
                item[2] = row[1]
                item[3] = row[2]
                item[4] = (row[3]-row[4])
                item[5] = row[5]
                item[6] = radio
                item[7] = sum4

                sum1 += item[3]
                sum2 += item[4]
                sum3 += item[5]

                rslist.append(item)

        cursor.close()
    except Exception as e:
        print(e)

    if qtype=='1':
        result = {"rslist":rslist}
        result.setdefault("shops",shops)
        result.setdefault("grpcode",grpcode)
        result.setdefault("grpname",grpname)
        result.setdefault("shopCode",shopcode)
        result.setdefault("sccode",sccode)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))

        return render(request, "user_sale_ctg_detail.html",result)
    else:
        return exportDetail(rslist,sum1,sum2,sum3)

def exportDetail(rslist,sum1,sum2,sum3):
    sname = "类别日销售列表"

    titles = [("日期","1000"),("小类编码","1000"),("小类名称","1000"),("销售数量","1000"),("实际销售","1000"),
              ("销售成本","1000"),("占比(%)","500"),("累计占比(%)","1000")]

    sumlist = ["合计","","",sum1,sum2,sum3,"100.00","100.0"]
    fmtlist = ["%Y-%m-%d",None,None,"0.00","0.000","0.000","0.00","0.0"]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "day_sale_category.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response