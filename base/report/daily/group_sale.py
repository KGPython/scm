#-*- coding:utf-8 -*-
__author__ = 'liubf'

import datetime
import decimal
import json

import xlwt3 as xlwt
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from base.models import BasPurLog
from base.report.common import Method as reportMth
from base.utils import DateUtil,MethodUtil as mtu
from base.report.common import Excel

def query(date):
    rbacDepartList, rbacDepart = reportMth.getRbacDepart(11)

    yesterday = date.strftime("%Y-%m-%d")
    # 查询当月销售
    try:
        conn = mtu.getMysqlConn()
        cur = conn.cursor()

        sqlKwholesale = '''
            select sdate,shopid,sum(salevalue) wsalevalue,sum(costvalue) wcostvalue,sum(salevalue-costvalue) wsalegain,sum(salevalue-costvalue)/sum(salevalue)*100 wgaintx from kwholesale where
             sdate between '{start}' and '{end}' and shopid in ({rbacDepart})
            group by sdate,shopid
        '''.format(start=yesterday, end=yesterday,rbacDepart=rbacDepart)

        cur.execute(sqlKwholesale)
        listKwholesale = cur.fetchall()

        sqlShopData = '''
              select sdate,shopid,b.Shopnm,tradeprice,TradeNumber,SaleValue,DiscValue,(SaleValue-DiscValue) sale,costvalue, (SaleValue-DiscValue-costvalue) salegain,
            (SaleValue-DiscValue-costvalue)/(SaleValue-DiscValue)*100 gaintx
            from RPT_SaleShop a,bas_shop b where  sdate between '{start}' and '{end}' and shopid in ({rbacDepart})
            and a.shopid=b.Shopcode and b.khbank='超市店 ';
        '''.format(start=yesterday, end=yesterday,rbacDepart=rbacDepart)

        cur.execute(sqlShopData)
        listShopData = cur.fetchall()

        for shop in listShopData :
            shopId = shop['shopid']
            for Kwholesale in listKwholesale :
                if Kwholesale['shopid'] == shopId:
                    shop['wsalevalue'] = Kwholesale['wsalevalue']
                    shop['wcostvalue'] = Kwholesale['wcostvalue']
                    shop['wsalegain'] = Kwholesale['wsalegain']
                    shop['wgaintx'] = Kwholesale['wgaintx']

        rlist = []
        sumDict = {}
        sum = {"shopid": "合计", "shopnm": "", "tradeprice": 0.0, "tradenumber": 0, "salevalue": 0.0, "discvalue": 0.0,
               "sale": 0.0,
               "costvalue": 0.0, "salegain": 0.0, "gaintx": "", "yhzhanbi": "", "wsalevalue": 0.0, "wcostvalue": 0.0,
               "wsalegain": 0.0, "wgaintx": ""}
        sumDict.setdefault("sum1", sum)

        unsumkey = ["gaintx", "wgaintx"]
        for obj in listShopData:
            if obj['shopid'] != 'C009':
                row = {}
                for key in obj.keys():
                    item = obj[key]
                    newkey = key.lower()
                    if item:
                        if isinstance(item, int) or isinstance(item, decimal.Decimal):
                            if newkey not in unsumkey:
                                row.setdefault(newkey, float(item))
                                sum[newkey] += float(item)
                            else:
                                row.setdefault(newkey, "%0.2f" % item + "%")
                        elif isinstance(item, datetime.datetime):
                            row.setdefault(newkey, item.strftime("%Y-%m-%d"))
                        else:
                            row.setdefault(newkey, item)
                    else:
                        row.setdefault(newkey, "")

                if row["sale"] > 0:
                    yhzhanbi = "%0.2f" % (row["discvalue"] * 100.0 / row["sale"]) + "%"
                else:
                    yhzhanbi = ""

                row.setdefault("yhzhanbi", yhzhanbi)
                rlist.append(row)

        if sum["sale"] > 0:
            sum["gaintx"] = "%0.2f" % (sum["salegain"] * 100.0 / sum["sale"]) + "%"
            sum["yhzhanbi"] = "%0.2f" % (sum["discvalue"] * 100.0 / sum["sale"]) + "%"
        else:
            sum["gaintx"] = ""
            sum["yhzhanbi"] = ""

        if sum["wsalevalue"] > 0:
            sum["wgaintx"] = "%0.2f" % (sum["wsalegain"] * 100.0 / sum["wsalevalue"]) + "%"
        else:
            sum["wgaintx"] = ""

        for key in sum.keys():
            item = sum[key]
            if not isinstance(item, str) and not isinstance(item, int):
                sum[key] = "%0.2f" % item
    except Exception as e:
        print(">>>>>>>>>>>>[异常]", e)
        # 计算月累加合计

    data = {"gslist":rlist,"sumDict":sumDict}
    return data

# @cache_page(60*60*4,cache='default',key_prefix='daily_group_sale')
@csrf_exempt
def index(request):
     qtype = mtu.getReqVal(request,"qtype","1")

     #操作日志
     if not qtype:
         qtype = "1"
     key_state = mtu.getReqVal(request, "key_state", '')
     if qtype=='2' and (not key_state or key_state!='2'):
         qtype = '1'

     path = request.path
     today = datetime.datetime.today()
     ucode = request.session.get("s_ucode")
     uname = request.session.get("s_uname")
     BasPurLog.objects.create(name="超市销售日报",url=path,qtype=qtype,ucode=ucode,uname=uname,createtime=today)

     date = DateUtil.get_day_of_day(-1)
     if qtype == "1":
         data = query(date)
         return render(request,"report/daily/group_sale.html",data)
     else:
         fname = date.strftime("%m.%d") + "_daily_group_sale.xls"
         return export(fname,date)


def export(fname,date):
    if not Excel.isExist(fname):
        data = query(date)
        createExcel(fname, data)
    res = {}
    res['fname'] = fname
    return HttpResponse(json.dumps(res))


def createExcel(fname, data):
    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)
    #写入sheet1 月累计销售报表
    writeDataToSheet1(wb,data['gslist'],data['sumDict'])
    Excel.saveToExcel(fname, wb)


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
