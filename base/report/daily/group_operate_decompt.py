#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import BasShopRegion
from django.http import HttpResponse
import datetime,calendar,decimal,time
import xlwt3 as xlwt

@csrf_exempt
def index(request):
     date = DateUtil.get_day_of_day(-15)
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
           "and groupid < 50 and groupid <> 42 GROUP BY dateid,shopid,groupid ORDER BY shopid,groupid,dateid "
     cur.execute(ysql)
     ylist = cur.fetchall()
     yshopdict,ygrpdict,ys_grplist = queryData(ylist,lastDay,date.day)

     #查询全月销售实际
     sale_sql = "SELECT sdate saledate,shopcode,LEFT(sccode,2) groupid,SUM(svalue-discount)/10000 sale,SUM(svalue-discount-scost)/10000 gain   "\
            " FROM sales_pro_temp WHERE sdate BETWEEN '"+start+" 00:00:00' AND '"+yesterday+" 23:59:59.999' AND shopcode IN ('"+shopids+"') "\
            "and LEFT(sccode,2) < 50 and LEFT(sccode,2) <> 42 GROUP BY shopcode,LEFT(sccode,2),DATE_FORMAT(sdate,'%Y-%m-%d') "
     cur.execute(sale_sql)
     sale_list = cur.fetchall()
     sshopdict,sgrpdict,ss_grplist = queryData(sale_list,lastDay,date.day)

     #查询批发销售单
     pf_sale_sql = "SELECT sdate saledate,shopid shopcode,LEFT(deptid,2) groupid,SUM(salevalue)/10000 sale,SUM(salevalue-costvalue)/10000 gain "\
            " FROM kwholesale WHERE sdate BETWEEN '"+start+" 00:00:00' AND '"+yesterday+" 23:59:59.999' "\
            "and LEFT(deptid,2) < 50 and LEFT(deptid,2) <> 42  GROUP BY DATE_FORMAT(sdate,'%Y-%m-%d'),shopid,LEFT(deptid,2) "\
            "ORDER BY shopid,LEFT(deptid,2),DATE_FORMAT(sdate,'%Y-%m-%d') "
     cur.execute(pf_sale_sql)
     pf_sale_list = cur.fetchall()
     pfshopdict,pfgrpdict,pfs_grplist = queryData(pf_sale_list,lastDay,date.day)

     #计算实际销售
     #门店
     shop_saledict,shop_zbdict,shop_sumlist = countSale(yshopdict,sshopdict,pfshopdict,lastDay)
     #课组
     group_saledict,group_zbdict,group_sumlist = countSale(ygrpdict,sgrpdict,pfgrpdict,lastDay)

     rslist = []
     grslist = []
     #计算合计占比
     countSumZb(shop_sumlist)
     countSumZb(group_sumlist)

     #合并list
     rslist.extend(shop_sumlist)
     grslist.extend(group_sumlist)

     mergeData(rslist,slist,yshopdict,shop_saledict,shop_zbdict)
     mergeGroupData(grslist,ygrpdict,group_saledict,group_zbdict,lastDay)

     formate_data(rslist)
     formate_data(grslist)

     #各个门店的课组每日明细
     srslist = []
     for row in slist:
         temp_rslist = []
         sid = row["shopid"]
         yshopdata = ys_grplist[sid]
         sshopdata = ss_grplist[sid]
         if sid in pfs_grplist:
            pfshopdata = pfs_grplist[sid]
         else:
            pfshopdata = {}

         shop_grp_saledict,shop_grp_zbdict,shop_grp_sumlist = countSale(yshopdata,sshopdata,pfshopdata,lastDay)

         countSumZb(shop_grp_sumlist)

         temp_rslist.extend(shop_grp_sumlist)

         mergeGroupData(temp_rslist,yshopdata,shop_grp_saledict,shop_grp_zbdict,lastDay)

         formate_data(temp_rslist)

         srslist.append(temp_rslist)

     shoplist = []
     for row in slist:
         item = {}
         item.setdefault("shopid",row["shopid"])
         item.setdefault("shopname",row["shopname"].strip())
         shoplist.append(item)

     #shoplist.sort(key=lambda x:x["shopid"])

     qtype = mtu.getReqVal(request,"qtype","1")
     if qtype == "1":
         return render(request, "report/daily/group_opt_decompt.html",{"rlist":rslist,"shoplist":shoplist,"grslist":grslist,"srslist":srslist})
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

def mergeData(rlist,slist,ydict,saledict,zbdict):
    for shop in slist:
        #预算
        row = {}
        row.setdefault("idname","{id}{name}".format(id=shop["shopid"],name=shop["shopname"]))
        yitem = ydict[shop["shopid"]]
        row = dict(row,**yitem)
        rlist.append(row)
        #实际
        row1 = {}
        row1.setdefault("idname","{id}{name}".format(id=shop["shopid"],name=shop["shopname"]))
        sitem1 = saledict[shop["shopid"]]
        row1 = dict(row1,**sitem1)
        rlist.append(row1)
        #占比
        row2 = {}
        row2.setdefault("idname","{id}{name}".format(id=shop["shopid"],name=shop["shopname"]))
        sitem2 = zbdict[shop["shopid"]]
        row2 = dict(row2,**sitem2)
        rlist.append(row2)

    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item,decimal.Decimal):
                rows[k] = "%0.2f" % float(item)

def mergeGroupData(grslist,ydict,saledict,zbdict,lastDay):
    #生鲜
    sx = [{"id":10,"name":"熟食"},{"id":11,"name":"水产"},{"id":12,"name":"蔬菜"},{"id":13,"name":"烘烤类"},{"id":14,"name":"鲜肉"},
          {"id":15,"name":"干果干货"},{"id":16,"name":"主食厨房"},{"id":17,"name":"水果"},{"id":18,"name":"蛋品"},{"id":19,"name":"家禽"}]
    #食品
    sp = [{"id":20,"name":"烟/酒"},{"id":21,"name":"饮料"},{"id":22,"name":"休闲食品"},{"id":23,"name":"冷冻冷藏"},
          {"id":24,"name":"冲调保健品"},{"id":25,"name":"粮油副食"}]
    #非食
    yp = [{"id":30,"name":"厨房用品类"},{"id":31,"name":"居家用品"},{"id":32,"name":"文化用品"},{"id":33,"name":"休闲用品"},
          {"id":34,"name":"清洁用品"},{"id":35,"name":"纸品"},{"id":36,"name":"非季节性服饰"},{"id":37,"name":"季节性服饰"},{"id":38,"name":"鞋"}]
    #家电
    jd = [{"id":40,"name":"3C"},{"id":41,"name":"大家电"},{"id":43,"name":"小家电"}]

    mergeBranchData(grslist,sx,ydict,saledict,zbdict,lastDay,"生鲜汇总")
    mergeBranchData(grslist,sp,ydict,saledict,zbdict,lastDay,"食品/杂货汇总")
    mergeBranchData(grslist,yp,ydict,saledict,zbdict,lastDay,"非食汇总")
    mergeBranchData(grslist,jd,ydict,saledict,zbdict,lastDay,"家电汇总")

def  mergeBranchData(rslist,glist,ydict,saledict,zbdict,lastDay,sumname):
    sum1 = initItem(lastDay)
    sum2 = initItem(lastDay)
    sumlist = []
    for group in glist:
        id = str(group["id"])
        #预算
        row = {}
        row.setdefault("idname","{id}{name}".format(id=id,name=group["name"]))
        if id in ydict:
            yitem = ydict[id]
        else:
            yitem = initItem(lastDay)
        row = dict(row,**yitem)
        rslist.append(row)
        #实际
        row1 = {}
        row1.setdefault("idname","{id}{name}".format(id=id,name=group["name"]))
        if id in saledict:
            sitem1 = saledict[id]
        else:
            sitem1 = initItem(lastDay)
        row1 = dict(row1,**sitem1)
        rslist.append(row1)
        #占比
        row2 = {}
        row2.setdefault("idname","{id}{name}".format(id=id,name=group["name"]))
        if id in zbdict:
            sitem2 = zbdict[id]
        else:
            sitem2 = initItem(lastDay)
        row2 = dict(row2,**sitem2)
        rslist.append(row2)

        countSum(yitem,sum1)
        countSum(sitem1,sum2)

    sumlist.append(sum1)
    sumlist.append(sum2)
    countSumZb(sumlist)

    sumlist[0]["idname"]=sumname
    sumlist[1]["idname"]=sumname
    sumlist[2]["idname"]=sumname
    rslist.extend(sumlist)

def formate_data(rlist):
    for rows in rlist:
        for k in rows.keys():
            item = rows[k]
            if isinstance(item,decimal.Decimal):
                rows[k] = "%0.2f" % float(item)

def countSum(item,sum):
     for key in item.keys():
            obj = item[key]
            if isinstance(obj,decimal.Decimal):
                if key in sum:
                    sum[key] += obj
                else:
                    sum.setdefault(key,obj)

def queryData(dlist,lastDay,yesterday):
    #实际：分别安门店，课组汇总
    sdict,gdict,sgdict = sumByType(dlist)
    #实际：竖转横
    shopdict,grpdict,shop_grplist = vertTohoriz(sdict,gdict,sgdict,lastDay,yesterday)
    return shopdict,grpdict,shop_grplist

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
     rdict3 = {}
     tempval = None
     tempval2 = None
     tempval3 = None
     tempval4 = None
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

        #门店明细
         shopid = row["shopcode"]
         if tempval3 != shopid:
             if shopid not in rdict3:
                rdict3.setdefault(shopid,{})

          #按课组
         shopgrpval = "{gid}_{sdate}".format(gid=row["groupid"],sdate=row["saledate"].day)
         if tempval4 != shopgrpval:
             item2 = {}
             item2.setdefault("saledate",row["saledate"])
             item2.setdefault("groupid",row["groupid"])
             item2.setdefault("sale",decimal.Decimal("0.0"))
             item2.setdefault("gain",decimal.Decimal("0.0"))
             rdict3[shopid].setdefault(shopgrpval,item2)

         rdict3[shopid][shopgrpval]["sale"] = row["sale"]
         rdict3[shopid][shopgrpval]["gain"] = row["gain"]
         tempval3 = shopid
         tempval4 = shopgrpval

     return rdict,rdict2,rdict3

def vertTohoriz(shopdict,grpdict,sgdict,lastDay,yesterday):
     #按门店
     yshopdict = getDataDict(shopdict,lastDay,yesterday,"shopcode")
     #按课组
     ygrpdict = getDataDict(grpdict,lastDay,yesterday,"groupid")
     #按各个门店的课组
     yshop_grpdict = {}
     for k in sgdict.keys():
         gdict = getDataDict(sgdict[k],lastDay,yesterday,"groupid")
         yshop_grpdict.setdefault(k,gdict)

     return yshopdict,ygrpdict,yshop_grpdict

def getDataDict(datadict,lastDay,yesterday,unitkey):
     rsdict = {}
     itemid = None
     for row in datadict.values():
        id = str(row[unitkey])
        if itemid != id:
            # if id not in rsdict:
            item = {}
            item.setdefault("m_all_sale",decimal.Decimal("0.00"))
            item.setdefault("m_daily_sale",decimal.Decimal("0.00"))
            item.setdefault("m_all_gain",decimal.Decimal("0.00"))
            item.setdefault("m_daily_gain",decimal.Decimal("0.00"))
            for d in range(1,lastDay+1):
                newkey = "sale_d{saledate}".format(saledate=d)
                newkey1 = "gain_d{saledate}".format(saledate=d)
                item.setdefault(newkey,decimal.Decimal("0.00"))
                item.setdefault(newkey1,decimal.Decimal("0.00"))
            rsdict.setdefault(id,item)
        day = row["saledate"].day
        key = "sale_d{saledate}".format(saledate=day)
        key1 = "gain_d{saledate}".format(saledate=day)
        rsdict[id][key] = row["sale"]
        rsdict[id][key1] = row["gain"]

        rsdict[id]["m_all_sale"] += row["gain"]
        rsdict[id]["m_all_gain"] += row["gain"]
        if day <= yesterday:
            rsdict[id]["m_daily_sale"] += row["gain"]
            rsdict[id]["m_daily_gain"] += row["gain"]

        itemid = id
     return rsdict

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