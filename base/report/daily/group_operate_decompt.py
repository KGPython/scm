#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import Kshopsale,BasShopRegion,Estimate
from django.http import HttpResponse
import datetime,calendar,decimal,time
import xlwt3 as xlwt

@csrf_exempt
def index(request):
     date = DateUtil.get_day_of_day(-1)
     start = (date.replace(day=1)).strftime("%Y-%m-%d")
     yesterday = date.strftime("%Y-%m-%d")
     lastDay = calendar.monthrange(date.year,date.month)[1]
     end = "{year}-{month}-{day}".format(year=date.year,month=date.month,day=lastDay)

     #查询所有超市门店
     slist = BasShopRegion.objects.values("shopid","shopname")\
                          .filter(shoptype=11).order_by("shopid")
     shopids = "','".join([shop["shopid"] for shop in slist])

     conn = mtu.getMysqlConn()
     cur = conn.cursor()
     #查询全月预算
     ysql = "SELECT dateid saledate,groupid,shopid shopcode,SUM(salevalue)/10000 sale,SUM(salegain)/10000 gain FROM Estimate " \
           " WHERE dateid BETWEEN '"+start+" 00:00:00' AND '"+end+" 23:59:59.999' AND deptlevelid=2   AND shopid IN ('"+shopids+"')  " \
           "and groupid < 50 and groupid <> 42 GROUP BY dateid,shopid,groupid ORDER BY dateid,shopid,groupid "
     yshopdict,ygrpdict = queryData(cur,ysql,lastDay,date.day)

     #查询全月销售实际
     sale_sql = "SELECT sdate saledate,shopcode,LEFT(sccode,2) groupid,SUM(svalue-discount)/10000 sale,SUM(svalue-discount-scost)/10000 gain   "\
            " FROM sales_pro_temp WHERE sdate BETWEEN '"+start+" 00:00:00' AND '"+yesterday+" 23:59:59.999' AND shopcode IN ('"+shopids+"') "\
            "and LEFT(sccode,2) < 50 and LEFT(sccode,2) <> 42 GROUP BY DATE_FORMAT(sdate,'%Y-%m-%d'),shopcode,LEFT(sccode,2) "
     sshopdict,sgrpdict = queryData(cur,sale_sql,lastDay,date.day)

     #查询批发销售单
     pf_sale_sql = "SELECT sdate saledate,shopid shopcode,LEFT(deptid,2) groupid,SUM(salevalue)/10000 sale,SUM(salevalue-costvalue)/10000 gain "\
            " FROM kwholesale WHERE sdate BETWEEN '"+start+" 00:00:00' AND '"+yesterday+" 23:59:59.999' "\
            "and LEFT(deptid,2) < 50 and LEFT(deptid,2) <> 42  GROUP BY DATE_FORMAT(sdate,'%Y-%m-%d'),shopid,LEFT(deptid,2) "\
            "ORDER BY DATE_FORMAT(sdate,'%Y-%m-%d'),shopid,LEFT(deptid,2) "
     pfshopdict,pfgrpdict = queryData(cur,pf_sale_sql,lastDay,date.day)

     #计算实际销售
     #门店
     saledict1,zbdict1,sumlist1 = countSale(yshopdict,sshopdict,pfshopdict,lastDay)
     #课组
     saledict2,zbdict2,sumlist2 = countSale(ygrpdict,sgrpdict,pfgrpdict,lastDay)

     sx = [10,11,12,13,14,15,16,17,18,19]   #生鲜汇总
     sp = [20,21,22,23,24,25]               #食品汇总
     yp = [30,31,32,33,34,35,36,37,38]      #用品汇总
     jd = [40,41,43]                        #家电汇总

     rlist = []
     #计算合计占比
     countSumZb(sumlist1)
     # countSumZb(sumlist2)

     #合并list
     rlist.extend(sumlist1)

     mergeData(rlist,slist,yshopdict,saledict1,zbdict1)

     shoplist = []
     for row in slist:
         item = {}
         item.setdefault("shopid",row["shopid"])
         item.setdefault("shopname",row["shopname"].strip())
         shoplist.append(item)

     qtype = mtu.getReqVal(request,"qtype","1")
     if qtype == "1":
         return render(request, "report/daily/group_opt_decompt.html",{"rlist":rlist,"shoplist":shoplist})
     # else:
     #     return export(request,rlist,sumDict,erlist,esumDict,yearlist,yearSumDict)

def countSumZb(rlist):
    if len(rlist)>1:
        sumdict = {}
        yitem = rlist[0]
        sitem = rlist[1]

        for key in yitem:
            est = yitem[key]
            if key in sitem:
                sale = sitem[key]
                if decimal.Decimal(est) > 0:
                    zb = mtu.convertToStr(decimal.Decimal(sale) * decimal.Decimal("100.0")/decimal.Decimal(est),"0.00",1) +"%"
                else:
                    zb = ""
            else:
                zb = ""
            sumdict.setdefault(key,zb)

        yitem.setdefault("idname","合计")
        sitem.setdefault("idname","合计")
        sumdict.setdefault("idname","合计")
        yitem.setdefault("codelable","计划")
        sitem.setdefault("codelable","实际达成")
        sumdict.setdefault("codelable","达成率")
        rlist.append(sumdict)

def mergeData(rlist,slist,ydict1,saledict1,zbdict1):
    for shop in slist:
        #预算
        row = {}
        row.setdefault("shopid",shop["shopid"])
        row.setdefault("idname","{shopid}{shopname}".format(shopid=shop["shopid"],shopname=shop["shopname"]))
        yitem = ydict1[shop["shopid"]]
        row = dict(row,**yitem)
        rlist.append(row)
        #实际
        row1 = {}
        row1.setdefault("shopid",shop["shopid"])
        row1.setdefault("idname","{shopid}{shopname}".format(shopid=shop["shopid"],shopname=shop["shopname"]))
        sitem1 = saledict1[shop["shopid"]]
        row1 = dict(row1,**sitem1)
        rlist.append(row1)
        #占比
        row2 = {}
        row2.setdefault("shopid",shop["shopid"])
        row2.setdefault("idname","{shopid}{shopname}".format(shopid=shop["shopid"],shopname=shop["shopname"]))
        sitem2 = zbdict1[shop["shopid"]]
        row2 = dict(row2,**sitem2)
        rlist.append(row2)

    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item,decimal.Decimal):
                rows[k] = "%0.2f" % float(item)


def queryData(cur,sql,lastDay,yesterday):
    cur.execute(sql)
    dlist = cur.fetchall()
    #实际：分别安门店，课组汇总
    shopdict,grpdict = sumByType(dlist)
    #实际：竖转横
    shopdict,grpdict = vertTohoriz(shopdict,grpdict,lastDay,yesterday)
    return shopdict,grpdict

def countSale(ydict,sdict1,sdict2,lastDay):
    rsdict = {}
    zbdict = {}

    sumlist = []
    ssumdict,ysumdict = {},{}
    sumlist.append(ysumdict)  #计划
    sumlist.append(ssumdict)  #实际

    for key in sdict1.keys():
        item = sdict1[key]
        if key in ydict:
            yitem = ydict[key]
        else:
            yitem = initItem(lastDay)
            ydict.setdefault(key,yitem)

        new,zbitem = {},{}
        new = dict(new,**item)

        for k in item:
            #实际销售
            obj = item[k]

            #批发销售单
            if key in sdict2:
                item2 = sdict2[key]
                if item2 and k in item2:
                    obj2 = item2[k]
                else:
                    obj2 = decimal.Decimal("0.00")
            else:
                 obj2 = decimal.Decimal("0.00")

            #真实销售 = 实际销售 + 批发销售
            val = obj+obj2
            new[k] = val

            #计划
            if k in yitem:
                yobj = yitem[k]
            else:
                yobj = decimal.Decimal("0.00")

            #占比
            if yobj>0:
                zb = mtu.convertToStr(val*decimal.Decimal("100.0")/yobj,"0.00",1)+"%"
                zbitem.setdefault(k,zb)
            else:
                zbitem.setdefault(k,"")

            #销售合计
            if k in ssumdict:
                ssumdict[k] += val
            else:
                ssumdict.setdefault(k,val)
            #计划合计
            if k in ysumdict:
                ysumdict[k] += yobj
            else:
                ysumdict.setdefault(k,yobj)

        yitem.setdefault("codelable","计划")
        new.setdefault("codelable","实际达成")
        zbitem.setdefault("codelable","达成率")
        rsdict.setdefault(key,new)
        zbdict.setdefault(key,zbitem)
    return rsdict,zbdict,sumlist

def sumByType(list):
     rdict = {}
     rdict2 = {}
     tempval = None
     tempval2 = None
     for row in list:
         #按门店
         shopval = "{sid}_{sdate}".format(sid=row["shopcode"],sdate=row["saledate"].day)
         if tempval != shopval:
             item = {}
             item.setdefault("saledate",row["saledate"])
             item.setdefault("shopcode",row["shopcode"])
             item.setdefault("sale",decimal.Decimal("0.0"))
             item.setdefault("gain",decimal.Decimal("0.0"))
             rdict.setdefault(shopval,item)

         rdict[shopval]["sale"] += row["sale"]
         rdict[shopval]["gain"] += row["gain"]
         tempval = shopval
         #按课组
         groupval = "{gid}_{sdate}".format(gid=row["groupid"],sdate=row["saledate"].day)
         if tempval2 != groupval:
             item2 = {}
             item2.setdefault("saledate",row["saledate"])
             item2.setdefault("groupid",row["groupid"])
             item2.setdefault("sale",decimal.Decimal("0.0"))
             item2.setdefault("gain",decimal.Decimal("0.0"))
             rdict2.setdefault(groupval,item2)

         rdict2[groupval]["sale"] += row["sale"]
         rdict2[groupval]["gain"] += row["gain"]
         tempval2 = groupval
     return rdict,rdict2

def vertTohoriz(shopdict,grpdict,lastDay,yesterday):
     #按门店
     yshopdict = {}
     itemshopid = None
     for row in shopdict.values():
        shopid = row["shopcode"]
        if itemshopid != shopid:
            if shopid not in yshopdict:
                item = {}
                # item.setdefault("shopid",shopid)
                item.setdefault("m_all_sale",decimal.Decimal("0.00"))
                item.setdefault("m_daily_sale",decimal.Decimal("0.00"))
                item.setdefault("m_all_gain",decimal.Decimal("0.00"))
                item.setdefault("m_daily_gain",decimal.Decimal("0.00"))
                for d in range(1,lastDay+1):
                    newkey = "sale_d{saledate}".format(saledate=d)
                    newkey1 = "gain_d{saledate}".format(saledate=d)
                    item.setdefault(newkey,decimal.Decimal("0.00"))
                    item.setdefault(newkey1,decimal.Decimal("0.00"))
                yshopdict.setdefault(shopid,item)

        day = row["saledate"].day
        key = "sale_d{saledate}".format(saledate=day)
        key1 = "gain_d{saledate}".format(saledate=day)
        yshopdict[shopid][key] = row["sale"]
        yshopdict[shopid][key1] = row["gain"]

        yshopdict[shopid]["m_all_sale"] += row["sale"]
        yshopdict[shopid]["m_all_gain"] += row["gain"]
        if day <= yesterday:
            yshopdict[shopid]["m_daily_sale"] += row["sale"]
            yshopdict[shopid]["m_daily_gain"] += row["gain"]
        itemshopid = shopid

     #按课组
     ygrpdict = {}
     itemgroupid = None
     for row in grpdict.values():
        groupid = str(row["groupid"])
        if itemgroupid != groupid:
            if groupid not in ygrpdict:
                item = {}
                # item.setdefault("groupid",groupid)
                item.setdefault("m_all_sale",decimal.Decimal("0.00"))
                item.setdefault("m_daily_sale",decimal.Decimal("0.00"))
                item.setdefault("m_all_gain",decimal.Decimal("0.00"))
                item.setdefault("m_daily_gain",decimal.Decimal("0.00"))
                for d in range(1,lastDay+1):
                    newkey = "sale_d{saledate}".format(saledate=d)
                    newkey1 = "gain_d{saledate}".format(saledate=d)
                    item.setdefault(newkey,decimal.Decimal("0.00"))
                    item.setdefault(newkey1,decimal.Decimal("0.00"))
                ygrpdict.setdefault(groupid,item)

        key = "sale_d{saledate}".format(saledate=row["saledate"].day)
        key1 = "gain_d{saledate}".format(saledate=row["saledate"].day)
        ygrpdict[groupid][key] = row["sale"]
        ygrpdict[groupid][key1] = row["gain"]

        ygrpdict[groupid]["m_all_sale"] += row["gain"]
        ygrpdict[groupid]["m_all_gain"] += row["gain"]
        if day <= yesterday:
            ygrpdict[groupid]["m_daily_sale"] += row["gain"]
            ygrpdict[groupid]["m_daily_gain"] += row["gain"]

        itemgroupid = groupid
     return yshopdict,ygrpdict

def initItem(lastDay):
    item = {}
    item.setdefault("m_all_sale",decimal.Decimal("0.00"))
    item.setdefault("m_all_gain",decimal.Decimal("0.00"))
    item.setdefault("m_daily_sale",decimal.Decimal("0.00"))
    item.setdefault("m_daily_gain",decimal.Decimal("0.00"))
    for d in range(1,lastDay+1):
        newkey = "sale_d{saledate}".format(saledate=d)
        newkey1 = "gain_d{saledate}".format(saledate=d)
        item.setdefault(newkey,decimal.Decimal("0.00"))
        item.setdefault(newkey1,decimal.Decimal("0.00"))
    return item