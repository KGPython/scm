#-*- coding:utf-8 -*-
__author__ = 'liubf'

import datetime,decimal
import xlrd,xlwt3 as xlwt

from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from base.views import findShop
from base.utils import MethodUtil as mtu

def index(request):

    return render(request,"user_sale_counter.html")

#查询列表
@csrf_exempt
def query(request):
    grpname = request.session.get("s_grpname","")
    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")

    shopcode = mtu.getReqVal(request,"shopCode","")
    teamcode = mtu.getReqVal(request,"teamcode","")     #条件无效
    teamname = mtu.getReqVal(request,"teamname","")     #条件无效
    start = mtu.getReqVal(request,"start")
    end = mtu.getReqVal(request,"end")
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
    #门店商品销售汇总
    #门店编号、总折扣、供应商折扣、销售金额、销售成本金额、销售数量
    sql = "SELECT tb1.shopcode,IFNULL(tb1.num,0),IFNULL(tb1.svalue,0),IFNULL(tb1.discount,0),IFNULL(tb1.scost,0),IFNULL(tb1.zzk,0) "
    sql += "FROM(SELECT a.shopcode,b.svalue,b.scost,b.num,b.discount,b.zzk "
    sql += "FROM(SELECT DISTINCT shopcode FROM sales_pro "
    sql += "WHERE grpcode='"+grpcode+"' AND ("+codes+") AND supercode='"+spercode+"'  and teamcode like  '%"+teamcode.strip()+"%' and teamname like  '%"+teamname.strip()+"%' ) a "     #
    sql += "LEFT JOIN(SELECT tb2.shopcode,SUM(tb2.svalue) svalue,SUM(tb2.scost)scost,SUM(tb2.num)num, "
    sql += "SUM(tb2.discount) discount, SUM(tb2.zzk) zzk FROM (SELECT shopcode,svalue,scost,num,discount,zzk FROM sales_pro "
    sql += "WHERE grpcode='"+grpcode+"' AND DATE_FORMAT(sdate,'%Y-%m-%d')>='"+start+"' AND DATE_FORMAT(sdate,'%Y-%m-%d')<='"+end+"'  and teamcode like  '%"+teamcode.strip()+"%' and teamname like  '%"+teamname.strip()+"%' "
    sql += "AND ("+codes+") AND (sstyle is not null and sstyle<>'' ) AND supercode='"+spercode+"' "   #
    sql += ") tb2 GROUP BY tb2.shopcode)b ON a.shopcode=b.shopcode) tb1 "

    sum1,sum2,sum3 = decimal.Decimal('0.0'),decimal.Decimal('0.0'),decimal.Decimal('0.0')

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        list = cursor.fetchall()
        #计算合计
        rslist = []
        if list:
            for row in list:
                item = ["","","",""]
                item[0] = row[0]
                item[1] = row[1]
                item[2] = row[2]-row[3]
                item[3] = row[4]

                sum1 += item[1]
                sum2 += item[2]
                sum3 += item[3]
                rslist.append(item)
        else:
            rslist = []

        cursor.close()
        # connection.close()
    except Exception as e:
        print(e)

    if qtype == "1":
        result = {"rslist":rslist}
        result.setdefault("grpcode",grpcode)
        result.setdefault("grpname",grpname)
        result.setdefault("shops",shops)
        result.setdefault("shopCode",shopcode)
        result.setdefault("teamcode",teamcode)
        result.setdefault("teamname",teamname)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sum1","%.2f" % sum1)
        result.setdefault("sum2","%.3f" % sum2)
        result.setdefault("sum3","%.3f" % sum3)
        return render(request, "user_sale_counter.html",result)
    else:

        return export(rslist,sum1,sum2,sum3)

#导出Excel
def export(rslist,sum1,sum2,sum3):
    sname = "门店－大类销售汇总"

    titles = [("门店名称","1000","shopid"),("销售数量","1000","promflag"),
              ("实际销售","1000","startdate"),("销售成本","1000","enddate")]

    fmtlist = [None,"0.00","0.000","0.000"]

    shopDict = findShop()

    dictlist = [shopDict,None,None,None]

    sumList = ["合计",sum1,sum2,sum3]

    book = mtu.exportXls(sname,titles,rslist,sumList,dictlist,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "sale_counter.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

 #查看详情
@csrf_exempt
def detail(request):
    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname","")

    shopCode = mtu.getReqVal(request,"shopCode")
    teamcode = mtu.getReqVal(request,"teamcode","")
    teamname = mtu.getReqVal(request,"teamname","")
    start = mtu.getReqVal(request,"start")
    end = mtu.getReqVal(request,"end")
    qtype = mtu.getReqVal(request,"qtype","1")

    #当月1号
    if not start:
        start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")
    #当日
    if not end:
        end = datetime.datetime.today().strftime("%Y-%m-%d")

    shopDict = findShop()
    if shopCode:
        codes = " shopcode='%s' " % shopCode
        shops = "%s" % shopDict[str(shopCode)]

    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')

    sum6 = decimal.Decimal('0.0')
    teamsv = decimal.Decimal('0.0')
    try:
        #销售成本总和
        sql = "select sum(IFNULL(scost,0)) scost "
        sql += " from sales_pro where grpcode = '"+grpcode+"' and ("+codes+") and sstyle<>''"
        sql += " and DATE_FORMAT(sdate,'%Y-%m-%d') >= '"+start+"' and DATE_FORMAT(sdate,'%Y-%m-%d') <= '"+end+"' and teamcode like '%"+teamcode.strip()+"%'"
        sql += " and supercode='"+spercode+"' and teamname like '%"+teamname.strip()+"%' "

        cursor = connection.cursor()
        cursor.execute(sql)
        rsobj = cursor.fetchone()

        if rsobj:
             teamsv = rsobj[0]

        #门店下商品大类销售汇总
        #总折扣、供应商折扣、实际销售、销售数量、销售成本、大类编码、销售日期、大类名称
        sql2 = "select IFNULL(tb2.zzk,0),IFNULL(tb2.discount,0),IFNULL(tb2.svalue,0),IFNULL(tb2.num,0),IFNULL(tb2.scost,0),tb2.bccode,tb2.sdate,org.orgname "
        sql2 += "    from(select sum(tb1.zzk) as zzk,sum(tb1.discount) as discount,sum(tb1.svalue) as svalue,sum(tb1.num) as num,"
        sql2 += "    sum(tb1.scost) as scost,tb1.bccode,date_format(tb1.sdate,'%Y-%m-%d') as sdate from("
        sql2 += "        select zzk,discount,svalue,num,scost,bccode,sdate "
        sql2 += "            from sales_pro  where grpcode='"+grpcode+"' and ("+codes+") and sstyle<>'' and DATE_FORMAT(sdate,'%Y-%m-%d') >= '"+start+"' "
        sql2 += "            and DATE_FORMAT(sdate,'%Y-%m-%d') <= '"+end+"' and teamcode like  '%"+teamcode.strip()+"%' and teamname like  '%"+teamname.strip()+"%' "
        sql2 += "            and supercode='"+spercode+"' and bccode is not null"
        sql2 += "     ) tb1  "
        sql2 += "     group by tb1.bccode,date_format(tb1.sdate,'%Y-%m-%d')"
        sql2 += ") tb2,bas_org org where tb2.bccode = org.orgcode order by tb2.bccode,tb2.sdate"

        # print(sql2)
        cursor.execute(sql2)
        list = cursor.fetchall()

        rslist = []
        outlist = []
        type1,type2 = "",""
        if list:
            for row in list:
                type2 = row[5]

                item = ["","","","","","","","",""]
                #销售数量、实际销售、销售成本、占比、累计占比
                if type1 != type2 and type1 != '':
                    itemsum = ["","","","","","","","",""]
                    itemsum[0] = '小计：'
                    itemsum[3] = sum1
                    itemsum[4] = sum2
                    itemsum[5] = sum3
                    itemsum[8] = '1'

                    outitemsum = itemsum[:]
                    outitemsum.pop()

                    rslist.append(itemsum)
                    outlist.append(outitemsum)

                item[0] = str(row[5])   #大类编码
                item[1] = str(row[7])   #大类名称
                item[2] = row[6]   #销售日期
                item[3] = row[3]   #销售数量
                item[4] = (row[2]-row[1])   #实际销售
                item[5] = row[4]   #销售成本
                if teamsv:
                    radio = (row[4] / teamsv * 100)
                    item[6] = str(radio)    #占比
                    sum6 += radio

                    item[7] = sum6   #累计占比

                item[8] = '2'  #类型

                type1 = type2

                sum1 += item[3]
                sum2 += item[4]
                sum3 += item[5]

                outitem = item[:]
                outitem.pop()
                rslist.append(item)
                outlist.append(outitem)

        cursor.close()
    except Exception as e:
        print(e)

    if qtype == "1":
        result = {"rslist":rslist}
        result.setdefault("grpcode",grpcode)
        result.setdefault("grpname",grpname)
        result.setdefault("shops",shops)
        result.setdefault("shopCode",shopCode)
        result.setdefault("teamcode",teamcode)
        result.setdefault("teamname",teamname)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))
        return render(request, "user_sale_counter_detail.html",result)
    else:
        return exportDetail(outlist,sum1,sum2,sum3)

def exportDetail(rslist,sum1,sum2,sum3):
    sname = "门店销售列表"

    titles = [("大类编码","1000","shopid"),("大类名称","1000","shopid"),("日期","1000","shopid"),
              ("销售数量","1000","promflag"),("实际销售","1000","startdate"),("销售成本","1000","enddate"),
              ("占比","500","enddate"),("累计占比","1000","enddate")]

    fmtlist = [None,None,"%Y-%m-%d","0.00","0.000","0.000","0.00","0.0"]

    sumList = ["合计",None,None,sum1,sum2,sum3,"100.00","100.00"]

    book = mtu.exportXls(sname,titles,rslist,sumList,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "sale_counter_detail.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

