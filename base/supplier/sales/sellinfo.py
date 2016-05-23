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
    pcode = mtu.getReqVal(request,"pcode","")
    pname = mtu.getReqVal(request,"pname","")
    tax = mtu.getReqVal(request,"tax","")
    barcode = mtu.getReqVal(request,"barcode","")
    orderstyle = mtu.getReqVal(request,"orderstyle","")
    qtype = mtu.getReqVal(request,"qtype","1")
    # fpcode = mtu.getReqVal(request,"fpcode")

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

    if not orderstyle:
         orderstyle = "pcode"

    sum = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    sum4 = decimal.Decimal('0.0')
    try:
        sql1 = "select sum(scost) scost from sales_pro where "
        sql1 += "grpcode='"+grpcode+"' and ("+codes+") "
        sql1 += "and ("+ccodes+") "
        sql1 += "and date_format(sdate,'%Y-%m-%d')>='"+start+"' "
        sql1 += "and date_format(sdate,'%Y-%m-%d')<='"+end+"' "
        sql1 += "and supercode='"+spercode+"' "
        if pcode:
            sql1 += "and pcode like '%"+pcode.strip()+"%' "
        if pname:
            sql1 += "and pname like '%"+pname.strip()+"%' "
        if tax:
            sql1 += "and tax='"+tax+"' "
        if barcode:
            sql1 += "and barcode like '%"+barcode.strip()+"%' "
        sql1 += "and sstyle<>'' "
        # sql1 += "and fpcode like '%%' "

        cursor = connection.cursor()
        cursor.execute(sql1)
        rsobj = cursor.fetchone()

        if rsobj:
            sum = rsobj[0]

        sql2 = "select pcode,barcode,pname,sccode,scname,classes,tax,num,svalue,discount,scost,zzk from(                                            "
        sql2 += "	select pcode,max(barcode) barcode,pname,sccode,scname,classes,tax,     "
        sql2 += "	sum(num) num,sum(svalue) svalue,sum(discount) discount  "
        sql2 += "	,sum(scost) scost,sum(zzk) zzk,      "
        sql2 += "	sstyle from(                         "
        sql2 += "		select * from sales_pro where                      "
        sql2 += "           grpcode='"+grpcode+"' and ("+codes+") "
        sql2 += "           and ("+ccodes+") "
        sql2 += "           and date_format(sdate,'%Y-%m-%d')>='"+start+"' "
        sql2 += "           and date_format(sdate,'%Y-%m-%d')<='"+end+"' "
        sql2 += "           and supercode='"+spercode+"' "
        if pcode:
            sql2 += "           and pcode like '%"+pcode.strip()+"%' "
        if pname:
            sql2 += "           and pname like '%"+pname.strip()+"%' "
        # sql2 += "           and fpcode like '%%' "
        if tax:
            sql2 += "           and tax='"+tax+"' "
        if barcode:
            sql2 += "           and barcode like '%"+barcode.strip()+"%' "
        sql2 += "           and sstyle<>'' "
        sql2 += "	) tb1 group by sstyle,pcode,pname,sccode,scname,classes,tax "
        sql2 += ") tb2 order by "+orderstyle+" desc   "

        cursor.execute(sql2)
        list = cursor.fetchall()

        rslist = []
        if list:
            for row in list:
                item = ["","","","","","","","","","","",""]

                if sum:
                    radio = (row[10] / sum * 100)   #占比
                    # item[12] = str(radio)
                    sum4 += radio   #累计占比

                    # item[13] = sum4

                item[0] = row[0]
                item[1] = row[1]
                item[2] = row[2]
                item[3] = row[3]
                item[4] = row[4]
                item[5] = row[5]
                item[6] = row[6]
                item[7] = row[7]
                item[8] = (row[8]-row[9])
                item[9] = row[10]
                item[10] = radio
                item[11] = sum4

                sum1 += item[7]
                sum2 += item[8]
                sum3 += item[9]

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
        result.setdefault("pcode",pcode)
        result.setdefault("pname",pname)
        result.setdefault("tax",tax)
        result.setdefault("barcode",barcode)
        result.setdefault("orderstyle",orderstyle)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))

        return render(request, "user_sale_sellinfo.html",result)
    else:
        return export(rslist,sum1,sum2,sum3)

def export(rslist,sum1,sum2,sum3):

    sname = "商品销售明细"

    titles = [("商品编号","1000"),("商品条码","1000"),("商品名称","3000"),("小类编码","1000"),("小类名称","1000"),("规格","500"),
              ("税率","500"),("销售数量","1000"),("实际销售","1000"),("销售成本","1000"),("占比(%)","500"),("累计占比(%)","500")]

    sumlist = ["合计","","","","","","",sum1,sum2,sum3,"100.00","100.0"]
    fmtlist = [None,None,None,None,None,None,"0.00","0.00","0.000","0.000","0.00","0.0"]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "sale_sellinfo.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

def detail(request):
    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname","")
    start = mtu.getReqVal(request,"start","")
    end = mtu.getReqVal(request,"end","")
    pcode = mtu.getReqVal(request,"pcode","")

    qtype = mtu.getReqVal(request,"qtype","1")
    # fpcode = mtu.getReqVal(request,"fpcode")

     #当月1号
    if not start:
        start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    #当日
    if not end:
        end = datetime.datetime.today().strftime("%Y-%m-%d")

    sum = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    sum4 = decimal.Decimal('0.0')
    try:

        sql1 = "select sum(scost),pname from(select scost,pname from sales_pro where grpcode='"+grpcode+"' "
        sql1 += "and date_format(sdate,'%Y-%m-%d')>='"+start+"' "
        sql1 += "and date_format(sdate,'%Y-%m-%d')<='"+end+"' "
        sql1 += "and supercode='"+spercode+"' and pcode= '"+pcode+"') tb1 "

        cursor = connection.cursor()
        cursor.execute(sql1)
        rsobj = cursor.fetchone()
        pname = ''

        if rsobj:
            sum = rsobj[0]
            pname = str(rsobj[1])

        sql2 = "select t1.shopcode,shopnm,num,svalue,discount,scost,zzk from(select shopcode,sum(scost) scost,"
        sql2 += "sum(zzk) zzk,sum(discount) discount,sum(svalue) svalue,sum(num) num "
        sql2 += "from(select * from sales_pro where grpcode='"+grpcode+"'"
        sql2 += "and date_format(sdate,'%Y-%m-%d')>='"+start+"' "
        sql2 += "and date_format(sdate,'%Y-%m-%d')<='"+end+"' "
        sql2 += "and supercode='"+spercode+"' and pcode= '"+pcode +"') t3 "
        sql2 += "group by shopcode)t1,bas_shop t2 where t2.grpcode='"+grpcode+"'"
        sql2 += "and t1.shopcode=t2.shopcode order by t1.shopcode"

        cursor.execute(sql2)
        list = cursor.fetchall()

        rslist = []
        if list:
            for row in list:
                item = ["","","","","","","","",""]

                if sum:
                    radio = (row[5] / sum * 100)   #占比
                    sum4 += radio     #累计占比

                item[0] = row[1]
                item[1] = row[2]
                item[2] = (row[3]-row[4])
                item[3] = row[5]
                item[4] = radio
                item[5] = sum4

                sum1 += item[1]
                sum2 += item[2]
                sum3 += item[3]

                rslist.append(item)

        cursor.close()
    except Exception as e:
        print(e)

    if qtype=='1':
        result = {"rslist":rslist}
        result.setdefault("grpcode",grpcode)
        result.setdefault("grpname",grpname)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("pcode",pcode)
        result.setdefault("pname",pname.strip())
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))

        return render(request, "user_sale_sellinfo_detail.html",result)
    else:
        return exportDetail(rslist,sum1,sum2,sum3,pname.strip())

def exportDetail(rslist,sum1,sum2,sum3,pname):
    sname = "单品"+pname+"销售汇总"

    titles = [("门店","2000"),("销售数量","1000"),("实际销售","1000"),("销售成本","1000"),
              ("销售成本占比","2000"),("销售成本累计占比","2000")]

    sumlist = ["合计",sum1,sum2,sum3,"100.00","100.00"]
    fmtlist = [None,"0.00","0.000","0.000","0.00","0.00"]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "sale_sellinfo_pro.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response