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
    grpname = request.session.get("s_grpname")

    shopcode = mtu.getReqVal(request,"shopCode","")
    sccode = mtu.getReqVal(request,"sccode","")
    start = mtu.getReqVal(request,"start","")
    end = mtu.getReqVal(request,"end","")
    pcode = mtu.getReqVal(request,"pcode","")
    pname = mtu.getReqVal(request,"pname","")
    barcode = mtu.getReqVal(request,"barcode","")
    orderstyle = mtu.getReqVal(request,"orderstyle","")
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

    if not orderstyle:
         orderstyle = "pcode"

    sum = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    try:

        cursor = connection.cursor()

        sql = "select pcode,barcode,pname,sccode,scname,classes,tax,num,svalue,discount,scost,date_format(sdate,'%Y-%m-%d') from(                                            "
        sql += "	select pcode,max(barcode) barcode,pname,sccode,scname,classes,tax,     "
        sql += "	sum(num) num,sum(svalue) svalue,sum(discount) discount  "
        sql += "	,sum(scost) scost,sdate,      "
        sql += "	sstyle from(                         "
        sql += "		select * from sales_pro where                      "
        sql += "           grpcode='"+grpcode+"' and ("+codes+") "
        sql += "           and ("+ccodes+") "
        sql += "           and date_format(sdate,'%Y-%m-%d')>='"+start+"' "
        sql += "           and date_format(sdate,'%Y-%m-%d')<='"+end+"' "
        sql += "           and supercode='"+spercode+"' "
        if pcode:
            sql += "           and pcode like '%"+pcode.strip()+"%' "
        if pname:
            sql += "           and pname like '%"+pname.strip()+"%' "
        if barcode:
            sql += "           and barcode like '%"+barcode.strip()+"%' "
        sql += "           and sstyle<>'' "
        sql += "	) tb1 group by sstyle,pcode,pname,classes,unit,sccode,scname,tax,date_format(sdate,'%Y-%m-%d') "
        sql += ") tb2 order by "+orderstyle+" desc   "

        cursor.execute(sql)
        list = cursor.fetchall()

        rslist = []
        if list:
            for row in list:
                item = ["","","","","","","","",""]

                item[0] = row[11]
                item[1] = row[0]
                item[2] = row[1]
                item[3] = row[2]
                item[4] = row[5]
                item[5] = row[6]
                item[6] = row[7]
                item[7] = row[8]-row[9]
                item[8] = row[10]

                sum1 += item[6]
                sum2 += item[7]
                sum3 += item[8]

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
        result.setdefault("barcode",barcode)
        result.setdefault("orderstyle",orderstyle)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))

        return render(request, "user_sale_pro.html",result)
    else:
        return export(rslist,sum1,sum2,sum3)


def export(rslist,sum1,sum2,sum3):
    sname = "单品销售汇总"

    titles = [("日期","1000"),("商品编号","1000"),("商品条码","1000"),("商品名称","3000"),("规格","500"),
              ("税率","500"),("销售数量","1000"),("实际销售","1000"),("销售成本","1000")]

    sumlist = ["合计","","","","","",sum1,sum2,sum3]
    fmtlist = [None,None,None,None,None,None,"0.00","0.000","0.000"]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "sale_product.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response