#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import BasShopRegion,BasPurLog
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

     mergeData(rslist,slist,yshopdict,shop_saledict,shop_zbdict,lastDay)
     mergeGroupData(grslist,ygrpdict,group_saledict,group_zbdict,lastDay)

     formate_data(rslist)
     formate_data(grslist)

     #各个门店的课组每日明细
     srslist = []
     for row in slist:
         temp_rslist = []
         sid = row["shopid"]
         if sid in ys_grplist:
            yshopdata = ys_grplist[sid]
         else:
            yshopdata = {}

         if sid in ss_grplist:
            sshopdata = ss_grplist[sid]
         else:
            sshopdata = {}

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

     qtype = mtu.getReqVal(request,"qtype","1")
     #操作日志
     if not qtype:
         qtype = "1"
     key_state = mtu.getReqVal(request, "key_state", '')
     if qtype == '2' and (not key_state or key_state != '2'):
         qtype = '1'
     path = request.path
     today = datetime.datetime.today();
     ucode = request.session.get("s_ucode")
     uname = request.session.get("s_uname")
     BasPurLog.objects.create(name="超市运营日分解",url=path,qtype=qtype,ucode=ucode,uname=uname,createtime=today)
     if qtype == "1":
         return render(request, "report/daily/group_opt_decompt.html",{"rlist":rslist,"shoplist":shoplist,"grslist":grslist,"srslist":srslist})
     else:
         return export(rslist,shoplist,grslist,srslist,date)

def export(rslist,shoplist,grslist,srslist,date):

    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)
    #写入sheet1 门店
    writeDataToSheet1(wb,rslist,date)
    #写入sheet2 类别
    writeDataToSheet2(wb,grslist,date)
    #写入sheet4 各个门店类别
    writeDataToSheetN(wb,shoplist,srslist,date)

    date = DateUtil.get_day_of_day(-1)
    outtype = 'application/vnd.ms-excel;'
    fname = date.strftime("%m.%d")+"grp_daily_opt_decompt"

    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response

def writeDataToSheet1(wb,rlist,date):
    year = date.year
    month = date.month

    sheet = wb.add_sheet("门店",cell_overwrite_ok=True)

    titles = [[("%s年%s月各店类别每日业绩指标分解达成表（单位：万元）" % (year,month),0,1,15)],
              [("门店编码",0,3,1),("日期",1,1,5)],
              [("%s月总指标" % month,1,2,1),("调整后销售指标",2,2,1),("累计计划销售达标率",3,2,1),("调整后毛利指标",4,2,1),("累计计划毛利达标率",5,2,1)],
              []]

    keylist = ['idname','codelable','m_all_sale','m_daily_sale','m_all_gain','m_daily_gain']
    widthlist = [1200,800,800,800,800,800]

    initExport(titles,keylist,widthlist,date)
    mtu.insertTitle2(sheet,titles,keylist,widthlist)
    mtu.insertCell2(sheet,4,rlist,keylist,None)

def writeDataToSheet2(wb,rlist,date):
    year = date.year
    month = date.month

    sheet = wb.add_sheet("类别",cell_overwrite_ok=True)

    titles = [[("%s年%s月各店类别每日业绩指标分解达成表（单位：万元）" % (year,month),0,1,15)],
              [("类别编码",0,3,1),("日期",1,1,5)],
              [("%s月总指标" % month,1,2,1),("调整后销售指标",2,2,1),("累计计划销售达标率",3,2,1),("调整后毛利指标",4,2,1),("累计计划毛利达标率",5,2,1)],
              []]

    keylist = ['idname','codelable','m_all_sale','m_daily_sale','m_all_gain','m_daily_gain']
    widthlist = [1200,800,800,800,800,800]

    initExport(titles,keylist,widthlist,date)
    mtu.insertTitle2(sheet,titles,keylist,widthlist)
    mtu.insertCell2(sheet,4,rlist,keylist,None)

def writeDataToSheetN(wb,shoplist,rlist,date):
    year = date.year
    month = date.month

    for i in range(len(shoplist)):
        shop = shoplist[i]
        sheetname = "%s%s" % (shop["shopid"][2:4],shop["shopname"])
        sheet = wb.add_sheet(sheetname,cell_overwrite_ok=True)

        titles = [[("%s年%s月各店类别每日业绩指标分解达成表（单位：万元）" % (year,month),0,1,15)],
                  [("类别编码",0,3,1),("日期",1,1,5)],
                  [("%s月总指标" % month,1,2,1),("调整后销售指标",2,2,1),("累计计划销售达标率",3,2,1),("调整后毛利指标",4,2,1),("累计计划毛利达标率",5,2,1)],
                  []]

        keylist = ['idname','codelable','m_all_sale','m_daily_sale','m_all_gain','m_daily_gain']
        widthlist = [1200,800,800,800,800,800]

        initExport(titles,keylist,widthlist,date)
        mtu.insertTitle2(sheet,titles,keylist,widthlist)
        mtu.insertCell2(sheet,4,rlist[i],keylist,None)

def initExport(titles,keylist,widthlist,date):
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year,month)[1]

    trow1 = titles[1]
    trow2 = titles[2]
    trow3 = titles[3]
    n = 6
    week_keys = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六","星期日"]
    for d in range(1,lastDay+1):
        t1 = ("{day}".format(day=d),n,1,2)
        trow1.append(t1)

        tempdate = datetime.datetime(year,month,d)
        week = week_keys[tempdate.weekday()]
        t2 = ("{week}".format(week=week),n,1,2)
        trow2.append(t2)

        t31 = ('销售',n,1,1)
        t32 = ('毛利',n+1,1,1)
        trow3.append(t31)
        trow3.append(t32)

        keylist.append("sale_d%s" % d)
        keylist.append("gain_d%s" % d)

        widthlist.append(800)
        widthlist.append(800)

        n += 2


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

def mergeData(rlist,slist,ydict,saledict,zbdict,lastDay):
    for shop in slist:
        sid = shop["shopid"]
        #预算
        row = {}
        row.setdefault("idname","{id}{name}".format(id=sid,name=shop["shopname"]))
        if sid in ydict:
            yitem = ydict[sid]
        else:
            yitem = initItem(lastDay)

        row = dict(row,**yitem)
        rlist.append(row)
        #实际
        row1 = {}
        row1.setdefault("idname","{id}{name}".format(id=sid,name=shop["shopname"]))
        if sid in saledict:
            sitem1 = saledict[sid]
        else:
            sitem1 = initItem(lastDay)

        row1 = dict(row1,**sitem1)
        rlist.append(row1)
        #占比
        row2 = {}
        row2.setdefault("idname","{id}{name}".format(id=sid,name=shop["shopname"]))
        if sid in zbdict:
             sitem2 = zbdict[sid]
        else:
            sitem2 = initItem(lastDay)

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
        sitem = sdict1[key]
        if key in ydict:
            yitem = ydict[key]
        else:
            yitem = initItem(lastDay)
            ydict.setdefault(key,yitem)

        newitem,zbitem = {},{}
        newitem = dict(newitem,**sitem)

        for k in sitem:
            #实际销售
            val1 = sitem[k]

            #批发销售单
            if key in sdict2:
                sitem2 = sdict2[key]
                if sitem2 and k in sitem2:
                    val2 = sitem2[k]
                else:
                    val2 = decimal.Decimal("0.00")
            else:
                val2 = decimal.Decimal("0.00")

            #真实销售 = 实际销售 + 批发销售
            totalval = val1+val2
            newitem[k] = totalval

            #计划
            if k in yitem:
                yobj = yitem[k]
                #占比
                if yobj>0:
                    zb = mtu.convertToStr(totalval*decimal.Decimal("100.0")/yobj,"0.00",1)+"%"
                    zbitem.setdefault(k,zb)
                else:
                    zbitem.setdefault(k,"")
            else:
                zbitem.setdefault(k,"")

            #销售合计
            if k in ssumdict:
                ssumdict[k] += totalval
            else:
                ssumdict.setdefault(k,totalval)

        newitem.setdefault("codelable","实际达成")
        zbitem.setdefault("codelable","达成率")
        rsdict.setdefault(key,newitem)
        zbdict.setdefault(key,zbitem)

    #计划合计
    for ykey in ydict.keys():
        yitem = ydict[ykey]
        for k in yitem.keys():
            yobj = yitem[k]
            if k in ysumdict:
                ysumdict[k] += yobj
            else:
                ysumdict.setdefault(k,yobj)
        yitem.setdefault("codelable","计划")
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

        rsdict[id]["m_all_sale"] += row["sale"]
        rsdict[id]["m_all_gain"] += row["gain"]
        if day <= yesterday:
            rsdict[id]["m_daily_sale"] += row["sale"]
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