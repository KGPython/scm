#-*- coding:utf-8 -*-
__author__ = 'liubf'

import decimal,datetime
import matplotlib
matplotlib.use('Agg')

import pylab,matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from base.views import findShop
from base.utils import MethodUtil as mtu

#查询日销售信息
@csrf_exempt
def query(request):

    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname")

    shopcode = mtu.getReqVal(request,"shopCode","")
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

    sum = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    sum4 = decimal.Decimal('0.0')
    try:
        sql1 = "select sum(ifnull(tb1.svalue,0)) from (select svalue from sales_pro " \
               " where grpcode='"+grpcode+"'  and ("+codes+") and DATE_FORMAT(sdate,'%Y-%m-%d')>='"+start+"'  and DATE_FORMAT(sdate,'%Y-%m-%d')<= '"+end+"' " \
               " and (sstyle <> '') and supercode='"+spercode+"' ) tb1"

        cursor = connection.cursor()
        cursor.execute(sql1)
        rsobj = cursor.fetchone()

        if rsobj:
            sum = rsobj[0]

        sql2 = "select date_format(tb1.sdate,'%Y-%m-%d') AS sdate,sum(tb1.svalue) AS svalue,sum(tb1.scost) AS scost," \
               "sum(tb1.num) AS num,sum(tb1.discount) AS discount " \
               "from (select * from sales_pro " \
               " where grpcode='"+grpcode+"'  and ("+codes+") and DATE_FORMAT(sdate,'%Y-%m-%d')>='"+start+"'  and DATE_FORMAT(sdate,'%Y-%m-%d')<= '"+end+"' "\
               " and (sstyle <> '') and supercode='"+spercode+"' )tb1 group by tb1.sdate order by tb1.sdate desc"

        cursor.execute(sql2)
        list = cursor.fetchall()

        rslist = []
        if list:
            for row in list:
                item = ["","","","","","","","",""]
                item[0]=row[0] #sdate
                item[1]=""
                item[2]=""
                item[3]=""
                item[4]=row[3]  #num
                item[5]=(row[1]-row[4]) #svalue - discount
                item[6]=row[2]  #scost

                if sum:
                    radio = (row[1] / sum * 100)
                    sum4 += radio

                item[7]=radio #占比
                item[8]=sum4 #累计占比

                sum1 += item[4]
                sum2 += item[5]
                sum3 += item[6]

                rslist.append(item)

        cursor.close()
    except Exception as e:
        print(e)
        rslist = []

    #折线图
    #imgfile = analysisImg(rslist,spercode,start,end)

    if qtype=='1':
        result = {"rslist":rslist}
        result.setdefault("shops",shops)
        result.setdefault("grpname",grpname)
        result.setdefault("shopCode",shopcode)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))
        # result.setdefault("imgfile",imgfile)
        return render(request, "user_sale_analysis.html",result)
    else:
        return export(rslist,sum1,sum2,sum3)

def analysisImg(rslist,spercode,start,end):
    # import matplotlib.font_manager as font_manager
    #
    # path = '/usr/share/fonts/winfonts/simfang.ttf'
    #
    # prop = font_manager.FontProperties(fname=path)
    # prop.set_weight = 'light'
    #
    # matplotlib.rc('font', family='sans-serif')
    # matplotlib.rc('font', serif='FangSong')
    # matplotlib.rc('text', usetex='false')
    # matplotlib.rcParams.update({'font.size': 12})


    #日期：结束日期 >= 27 ，取每月的周三
    #      13< 。。。< 27 , 取奇数
    #      6 <=  。。。<= 13 ,顺序数
    #      。。。<6 ,每日00：00，12：00

    list = []
    if rslist:
        for item in rslist:
            sd =  pylab.datestr2num(item[0])
            dict = (sd,float(item[6].quantize(decimal.Decimal('0.0'))))
            list.append(dict)

    #排序
    dict= sorted(list, key=lambda d:d[0])

    x,xt,y = [],[],[]
    for item in dict:
        x.append(item[0])
        y.append(item[1])
    if x:
        xmin = min(x)
        xmax = max(x)
        plt.xlim(xmin,xmax)

    if y:
        ymin = min(y)
        ymax = max(y)
        plt.ylim(ymin,ymax)

    plt.plot(x, y, linestyle='-',color="red")

    ds = [pylab.num2date(d) for d in x]
    xt = [(d.strftime('%d')+"-"+d.strftime("%m")+"月") for d in ds]
    plt.xticks(x,xt)
    plt.xlabel('时间(天)')
    plt.ylabel('金额(元)')
    plt.title('供应商日销售汇总折线图')
    plt.grid(True)


    root = settings.BASE_DIR
    filepath = "/static/image/daysale/" + spercode+".png"
    plt.savefig(root+filepath)
    return  filepath


#导出Excel
def export(outlist,sum1,sum2,sum3):
    sname = "日销售汇总列表"
    titles = [("日期","1000"),("门店明细","1000"),("单品明细","1000"),("大类明细","1000"),("销售数量","1000"),("实际销售","1000"),
              ("销售成本","1000"),("销售成本占比(%)","2000"),("销售成本累计占比(%)","3000")]

    sumlist = ["合计","门店合计","单品合计","大类合计",sum1,sum2,sum3,"100.00","100.00"]
    fmtlist = [None,None,None,None,"0.00","0.00","0.00","0.00","0.0"]

    book = mtu.exportXls(sname,titles,outlist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "day_sale_analysis.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

@csrf_exempt
def detail1(request):

    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname")

    shopcode = mtu.getReqVal(request,"shopCode")
    sdate = mtu.getReqVal(request,"sdate")
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

    type = ""
    if sdate:
        start = sdate;
        end = sdate;
        type = '日'
    else:
        sdate = ""

    sql ="SELECT t1.scost,t1.svalue,t1.num,t1.shopcode,t2.shopnm,t1.discount FROM(             "
    sql +="	SELECT SUM(scost) scost,SUM(svalue) svalue,SUM(num) num,shopcode,SUM(discount) discount FROM ( "
    sql +="		SELECT * FROM sales_pro WHERE grpcode='"+grpcode+"' AND sstyle<>''        "
    sql +="	        AND ("+codes+") AND   "
    sql +="		DATE_FORMAT(sdate,'%Y-%m-%d')>= '"+start+"' AND "
    sql +="		DATE_FORMAT(sdate,'%Y-%m-%d')<= '"+end+"' "
    sql +="	        AND supercode = '"+spercode+"'  "
    sql +="	        ORDER BY shopcode  "
    sql +="	) t3  "
    sql +="	GROUP BY shopcode "
    sql +=") t1 "
    sql +="LEFT JOIN bas_shop t2 ON t1.shopcode=t2.shopcode "
    sql +="WHERE t2.grpcode='"+grpcode+"' "

    cursor = connection.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()

    sum1 = decimal.Decimal("0.0")
    sum2 = decimal.Decimal("0.0")
    sum3 = decimal.Decimal("0.0")
    rslist = []
    if list:
        for row in list:
            item = ["","","","",""]
            item[0] = row[3]
            item[1] = row[4]
            item[2] = row[2]
            item[3] = (row[1] - row[5])
            item[4] = row[0]

            sum1 += row[2]
            sum2 += (row[1]- row[5])
            sum3 += row[0]

            rslist.append(item)

    if qtype=='1':
        result = {"list":rslist}
        result.setdefault("type",type)
        result.setdefault("grpname",grpname)
        result.setdefault("shops",shops)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sdate",sdate)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))
        return render(request, "user_sale_analysis_dtlshop.html",result)
    else:
        return exportDetail1(rslist,sum1,sum2,sum3,type)

def exportDetail1(result,sum1,sum2,sum3,type):
    sname = "销售汇总―柜组"+type+"销售汇总"

    titles = [("门店编号","1000"),("门店名称","3000"),("销售数量","1000"),("实际销售","1000"),
              ("销售成本","1000")]

    sumlist = ["合计","",sum1,sum2,sum3]
    fmtlist = [None,None,"0.00","0.000","0.000"]

    book = mtu.exportXls(sname,titles,result,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "day_sale_analysis_shop.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

@csrf_exempt
def detail2(request):
    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname")

    shopcode = mtu.getReqVal(request,"shopcode")
    sdate = mtu.getReqVal(request,"sdate")
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

    type = ""
    if sdate:
        start = sdate;
        end = sdate;
        type = '日'
    else:
        sdate = ""

    sv = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    try:
        sql ="select sum(tb1.scost) scost from(select * from sales_pro where "
        sql +="grpcode='"+grpcode+"' and ("+codes+") "
        sql +="and DATE_FORMAT(sdate,'%Y-%m-%d')>='"+start+"' "
        sql+="and DATE_FORMAT(sdate,'%Y-%m-%d')<='"+end+"' "
        sql +="and supercode='"+spercode+"' and (sstyle<>'')) tb1 "

        cursor = connection.cursor()
        cursor.execute(sql)
        rsobj = cursor.fetchone()

        if rsobj:
            sv = rsobj[0]

        sql2 = "select tb1.pcode,tb1.pname,max(tb1.barcode) as  barcode,tb1.classes,tb1.unit,sum(tb1.num) as num,"
        sql2 += "sum(tb1.svalue) as svalue,sum(tb1.discount) as discount,sum(tb1.scost) as scost,tb1.tax,tb1.sstyle "
        sql2 += "from(select * from sales_pro where "
        sql2 += "grpcode='"+grpcode+"' and ("+codes+") "
        sql2 += "and DATE_FORMAT(sdate,'%Y-%m-%d')>='"+start+"' "
        sql2 += "and DATE_FORMAT(sdate,'%Y-%m-%d')<='"+end+"' "
        sql2 += "and supercode='"+spercode+"' and (sstyle<>'') order by pcode) tb1 "
        sql2 += "group by tb1.tax,tb1.sstyle,tb1.pcode,tb1.pname,tb1.unit,tb1.classes "

        cursor.execute(sql2)
        list = cursor.fetchall()
        rslist = []
        if list:
            #tax #sstyle#pcode#pname#barcode#scost#svalue#discount#classes#unit#num
            for row in list:
                item = ["","","","","","","","",""]
                item[0] = row[0]
                item[1] = row[2]
                item[2] = row[1]
                item[3] = row[3]
                item[4] = row[4]
                item[5] = row[5]
                item[6] = row[6]-row[7]
                item[7] = row[8]
                item[8] = row[9]

                sum1 += item[5]
                sum2 += item[6]
                sum3 += item[7]

                rslist.append(item)

        cursor.close()
    except Exception as e:
        print(e)

    if qtype=='1':
        result = {"list":list}
        result.setdefault("type",type)
        result.setdefault("grpname",grpname)
        result.setdefault("shops",shops)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sdate",sdate)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))
        return render(request, "user_sale_analysis_dtlpro.html",result)
    else:
         return exportDetail2(rslist,sum1,sum2,sum3,type)

def exportDetail2(rslist,sum1,sum2,sum3,type):

    sname = " 销售汇总―单品"+type+"销售汇总"

    titles = [("商品编号","1000"),("商品条码","1000"),("商品名称","3000"),("规格","500"),("单位","500"),
              ("销售数量","1000"),("实际销售","1000"),("销售成本","1000"),("税率","500")]

    sumlist = ["合计","","","","",sum1,sum2,sum3,""]
    fmtlist = [None,None,None,None,None,"0.00","0.000","0.000",None]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "day_sale_analysis_pro.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response

@csrf_exempt
def detail3(request):

    spercode = request.session.get("s_suppcode")
    grpcode = request.session.get("s_grpcode")
    grpname = request.session.get("s_grpname")

    shopcode = mtu.getReqVal(request,"shopcode")
    sdate = mtu.getReqVal(request,"sdate")
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

    type = ""
    if sdate:
        start = sdate;
        end = sdate;
        type = '日'
    else:
        sdate = ""

    sv = decimal.Decimal('0.0')
    sum1 = decimal.Decimal('0.0')
    sum2 = decimal.Decimal('0.0')
    sum3 = decimal.Decimal('0.0')
    try:
        sql = "select tb1.teamcode,tb1.teamname,sum(tb1.num) as num ,sum(tb1.svalue) as svalue,sum(tb1.discount) as discount "
        sql += ",sum(tb1.scost) as scost,sum(tb1.zzk) as zzk from "
        sql += "(select * from sales_pro where "
        sql += "grpcode='"+grpcode+"' and ("+codes+") and ( "
        sql += "sstyle<>'' ) and DATE_FORMAT(sdate,'%Y-%m-%d')>='"+start+"' "
        sql += "and DATE_FORMAT(sdate,'%Y-%m-%d')<='"+end+"' "
        sql += "and supercode='"+spercode+"' order by teamcode) tb1 "
        sql += "group by tb1.teamcode,tb1.teamname "

        cursor = connection.cursor()
        cursor.execute(sql)
        list = cursor.fetchall()
        outlist = []
        if list:
            for row in list:
                item = ["","","","",""]
                item[0] = row[0]
                item[1] = row[1]
                item[2] = row[2]
                item[3] = row[3]-row[4]
                item[4] = row[5]

                sum1 += item[2]
                sum2 += item[3]
                sum3 += item[4]

                outlist.append(item)

        cursor.close()
    except Exception as e:
        print(e)

    if qtype=='1':
        result = {"rslist":list}
        result.setdefault("type",type)
        result.setdefault("grpname",grpname)
        result.setdefault("shops",shops)
        result.setdefault("start",start)
        result.setdefault("end",end)
        result.setdefault("sdate",sdate)
        result.setdefault("sum1",sum1.quantize(decimal.Decimal('0.00')))
        result.setdefault("sum2",sum2.quantize(decimal.Decimal('0.000')))
        result.setdefault("sum3",sum3.quantize(decimal.Decimal('0.000')))
        return render(request, "user_sale_analysis_dtlgz.html",result)
    else:
         return exportDetail3(outlist,sum1,sum2,sum3,type)

def exportDetail3(rslist,sum1,sum2,sum3,type):
    sname = "销售汇总―大类"+type+"销售汇总"

    titles = [("大类编号","1000"),("大类名称","1000"),("销售数量","1000"),
              ("实际销售","1000"),("销售成本","1000")]

    sumlist = ["合计","",sum1,sum2,sum3]
    fmtlist = [None,None,"0.00","0.000","0.000"]

    book = mtu.exportXls(sname,titles,rslist,sumlist,None,fmtlist)

    outtype = 'application/vnd.ms-excel'
    fname = "day_sale_analysis_gz.xls"
    response = mtu.getResponse(HttpResponse(),outtype,fname)
    book.save(response)
    return response