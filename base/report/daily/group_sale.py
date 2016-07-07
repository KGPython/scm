#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import Kshopsale,BasShopRegion,Estimate,BasPurLog
from django.db import connection
from django.http import HttpResponse
import datetime,calendar,decimal
import xlwt3 as xlwt

@csrf_exempt
def index(request):
     date = DateUtil.get_day_of_day(-1)
     yesterday = date.strftime("%Y-%m-%d")

     #查询当月销售
     try:
         sql = "CALL k_d_wholesale ('{start}','{end}') ".format(start=yesterday,end=yesterday)
         conn = mtu.getMysqlConn()
         cur = conn.cursor()
         cur.execute(sql)
         list = cur.fetchall()
         rlist = []
         sumDict = {}
         sum = {"shopid":"合计","shopnm":"","tradeprice":0.0,"tradenumber":0,"salevalue":0.0,"discvalue":0.0,"sale":0.0,
                    "costvalue":0.0,"salegain":0.0,"gaintx":"","yhzhanbi":"","wsalevalue":0.0,"wcostvalue":0.0,"wsalegain":0.0,"wgaintx":""}
         sumDict.setdefault("sum1",sum)

         unsumkey = ["gaintx","wgaintx"]
         for obj in list:
            row = {}
            for key in obj.keys():
                item = obj[key]
                newkey = key.lower()
                if item:
                    if isinstance(item,int) or isinstance(item,decimal.Decimal):
                        if newkey not in unsumkey:
                            row.setdefault(newkey,float(item))
                            sum[newkey] += float(item)
                        else:
                            row.setdefault(newkey,"%0.2f" % item+"%")
                    elif isinstance(item,datetime.datetime):
                        row.setdefault(newkey,item.strftime("%Y-%m-%d"))
                    else:
                        row.setdefault(newkey,item)
                else:
                    row.setdefault(newkey,"")

            if row["sale"]>0:
                yhzhanbi = "%0.2f" % (row["discvalue"]*100.0/row["sale"]) + "%"
            else:
                yhzhanbi = ""

            row.setdefault("yhzhanbi",yhzhanbi)
            rlist.append(row)

         if sum["sale"] > 0:
             sum["gaintx"] = "%0.2f" % (sum["salegain"]*100.0/sum["sale"]) + "%"
             sum["yhzhanbi"] = "%0.2f" % (sum["discvalue"]*100.0/sum["sale"]) + "%"
         else:
            sum["gaintx"] = ""
            sum["yhzhanbi"] = ""

         if sum["wsalevalue"] > 0:
            sum["wgaintx"] = "%0.2f" % (sum["wsalegain"]*100.0/sum["wsalevalue"]) + "%"
         else:
            sum["wgaintx"] = ""

         for key in sum.keys():
             item = sum[key]
             if not isinstance(item,str) and not isinstance(item,int):
                 sum[key] = "%0.2f" % item
     except Exception as e:
        print(">>>>>>>>>>>>[异常]",e)
     #计算月累加合计
     qtype = mtu.getReqVal(request,"qtype","1")

     #操作日志
     if not qtype:
         qtype = "1"
     key_state = mtu.getReqVal(request, "key_state", '')
     if qtype=='2' and (not key_state or key_state!='2'):
         qtype = '1'

     path = request.path
     today = datetime.datetime.today();
     ucode = request.session.get("s_ucode")
     uname = request.session.get("s_uname")
     BasPurLog.objects.create(name="超市销售日报",url=path,qtype=qtype,ucode=ucode,uname=uname,createtime=today)

     if qtype == "1":
         return render(request,"report/daily/group_sale.html",{"gslist":rlist,"sumDict":sumDict})
     else:
         return export(rlist,sumDict)

def export(rlist,sumList):

    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)

    #写入sheet1 月累计销售报表
    writeDataToSheet1(wb,rlist,sumList)

    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d")+"group_daily_sale"

    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response

def writeDataToSheet1(wb,rlist,sumDict):
    date = DateUtil.get_day_of_day(-1)
    yesterday = date.strftime("%Y-%m-%d")

    sheet = wb.add_sheet("宽广集团销售日报表",cell_overwrite_ok=True)

    titles = [[("宽广集团销售日报表",2,1,13)],
              [("数据日期：",0,1,2),(yesterday,2,1,1),("单位：元",4,1,1)],
              [("机构编码",0,2,1),("机构名称",1,2,1),("POS销售数据",3,1,9),("批发销售数据",4,1,4)],
              [("总客流量",2,1,1),("平均客单价",3,1,1),("销售金额",4,1,1),("折扣金额",5,1,1),("实际销售",6,1,1),("销售成本",7,1,1),
               ("毛利",8,1,1),("毛利率",9,1,1),("优惠占比",10,1,1),("实际销售",11,1,1),("销售成本",12,1,1),("毛利",13,1,1),("毛利率",14,1,1)],
            ]

    keylist = ['shopid','shopnm','tradenumber','tradeprice','salevalue','discvalue','sale','costvalue',
               'salegain','gaintx','yhzhanbi','wsalevalue','wcostvalue','wsalegain',
               'wgaintx']

    widthList = [600,400,1000,800,400,800,800,800,800,800,800,800,800,800,800]

    mtu.insertTitle2(sheet,titles,keylist,widthList)
    count = mtu.insertCell2(sheet,4,rlist,keylist,None)
    mtu.insertSum2(sheet,keylist,count,sumDict,2)
