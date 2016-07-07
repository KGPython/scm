# -*- coding:utf-8 -*-
__author__ = 'chen'

from django.shortcuts import render
from django.http import HttpResponse
from base.utils import DateUtil,MethodUtil as mtu
from base.models import BasPurLog
import datetime,decimal,calendar
import xlwt3 as xlwt

def inidex(request):
    shopTop = []
    shopTopTotal = {'shopid':'合计','shopname':''}

    conn = mtu.getMysqlConn()
    cur = conn.cursor()

    today = datetime.date.today()
    monthFirst = datetime.date.today().replace(day=1)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    if(str(today)[8:10]=='01'):
        monthFirst = datetime.date(datetime.date.today().year,datetime.date.today().month,1)
        today = datetime.date(datetime.date.today().year,datetime.date.today().month,1) - datetime.timedelta(days=1)
    todayStr = today.strftime('%y-%m-%d')
    monthFirstStr = str(monthFirst)
    yesterdayStr = yesterday.strftime('%y-%m-%d')

    #月累计报损
    sqlMonthTotal = 'select shopid,shopname,sum(costvalue) costvalueSum,sum(lostvalue) lostvalueSum,(sum(lostvalue)/sum(costvalue)) lrateSum ' \
                    'from KGshop17lost ' \
                    'where sdate between "'+monthFirstStr+'" and "'+todayStr+'" ' \
                    'group by shopid order by shopid '
    cur.execute(sqlMonthTotal)
    shopTop = cur.fetchall()

    #每日报损
    sqlDaily = 'select sdate,shopid,costvalue,lostvalue,lrate ' \
               'from KGshop17lost ' \
               'where sdate between "'+monthFirstStr+'" and "'+todayStr+'" ' \
               'order by sdate '
    cur.execute(sqlDaily)
    listDaily = cur.fetchall()
    #计算纵向合计、格式化数据、拼接月累计报损和每日报损
    for obj1 in shopTop:
        obj1['lostvalueSum'] = float(obj1['lostvalueSum']) if obj1['lostvalueSum'] else 0
        if 'lostvalueSum' in shopTopTotal:
            shopTopTotal['lostvalueSum'] += obj1['lostvalueSum']
        else:
            shopTopTotal['lostvalueSum'] = obj1['lostvalueSum']

        obj1['costvalueSum'] = float(obj1['costvalueSum']) if obj1['costvalueSum'] else 0
        if 'costvalueSum' in shopTopTotal:
            shopTopTotal['costvalueSum'] += obj1['costvalueSum']
        else:
            shopTopTotal['costvalueSum'] = obj1['costvalueSum']

        obj1['lrateSum'] = str(float('%0.2f'%(obj1['lrateSum']*100)))+'%' if obj1['lrateSum'] else '0.00%'
        shopTopTotal['lrateSum'] = shopTopTotal['lostvalueSum']/shopTopTotal['costvalueSum']
        shopTopTotal['lrateSum'] = str(float('%0.2f'%(shopTopTotal['lrateSum']*100)))+'%'
        for obj2 in listDaily:
            date = str(obj2['sdate'])[8:10]
            if obj1['shopid'] == obj2['shopid']:
                obj1['costvalue_'+date] = float('%0.2f'%obj2['costvalue']) if obj2['costvalue'] else 0
                if 'costvalue_'+date in shopTopTotal:
                    shopTopTotal['costvalue_'+date] += obj1['costvalue_'+date]
                    shopTopTotal['costvalue_'+date] = float('%0.2f'%shopTopTotal['costvalue_'+date])
                else:
                    shopTopTotal['costvalue_'+date] = obj1['costvalue_'+date]

                obj1['lostvalue_'+date] = float('%0.2f'%obj2['lostvalue']) if obj2['lostvalue'] else 0
                if 'lostvalue_'+date in shopTopTotal:
                    shopTopTotal['lostvalue_'+date] += obj1['lostvalue_'+date]
                    shopTopTotal['lostvalue_'+date] = float('%0.2f'%shopTopTotal['lostvalue_'+date])
                else:
                    shopTopTotal['lostvalue_'+date] = obj1['lostvalue_'+date]

                obj1['lrate_'+date] = str(float(obj2['lrate']*100))+'%' if obj2['lrate'] else '0.00%'
                shopTopTotal['lrate_'+date] = (shopTopTotal['lostvalue_'+date]/shopTopTotal['costvalue_'+date])
                shopTopTotal['lrate_'+date] = str(float('%0.2f'%(shopTopTotal['lrate_'+date]*100)))+'%'

    TotalDict = {'shopTopTotal':shopTopTotal}
    qtype = mtu.getReqVal(request,"qtype","1")

    # 操作日志
    if not qtype:
        qtype = "1"
    key_state = mtu.getReqVal(request, "key_state", '')
    if qtype == '2' and (not key_state or key_state != '2'):
        qtype = '1'
    path = request.path
    today = datetime.datetime.today();
    ucode = request.session.get("s_ucode")
    uname = request.session.get("s_uname")
    BasPurLog.objects.create(name="超市水果报损率", url=path, qtype=qtype, ucode=ucode,uname=uname, createtime=today)

    if qtype== "1":
        return render(request,'report/daily/fruit_lost.html',locals())
    else:
        return export(request,shopTop,TotalDict)


def export(request,shopTop,TotalDict):
    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)
    #写入sheet1
    writeDataToSheet1(wb,shopTop,TotalDict)
    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d")+"zero_daily_operate"
    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response

def writeDataToSheet1(wb,shopTop,TotalDict):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year,month)[1]

    sheet = wb.add_sheet("（月）水果报损率日报",cell_overwrite_ok=True)

    titles = [[("（%s月）水果报损率日报" % month,0,1,15)],
              [("门店编号",0,2,1),("门店名称",1,2,1),("月累计报损",2,1,3)],
              [('成本金额',2,1,1),('销售成本金额',3,1,1),('报损率',4,1,1),]
              ]

    keylist = ['shopid','shopname','lostvalueSum','costvalueSum','lrateSum']

    widthList = [600,1100,600,600,600,600]

    trow1 = titles[1]
    trow2 = titles[2]

    n = 5 #1日单元格开始位置
    for d in range(1,lastDay+1):
        trow1.append((str(d)+'日',n,1,3))
        trow2.append(('成本金额',n,1,1))
        trow2.append(('销售成本金额',n+1,1,1))
        trow2.append(('报损率',n+2,1,1))
        widthList.append(600)
        widthList.append(400)
        widthList.append(400)
        widthList.append(400)
        n += 3  #每日单元格数量
        dStr = '0'+str(d) if d<10 else str(d)
        keylist.append('lostvalue_'+dStr)
        keylist.append('costvalue_'+dStr)
        keylist.append('lrate_'+dStr)

    #日销售报表
    mtu.insertTitle2(sheet,titles,keylist,widthList)
    mtu.insertCell2(sheet,3,shopTop,keylist,None)
    titlesLen = len(titles)
    listTopLen = len(shopTop)
    mtu.insertSum2(sheet,keylist,titlesLen+listTopLen,TotalDict,2)


def formatDate(dict):
    for key in dict.keys():
        #转换数据格式
        obj = dict[key]
        if obj is None:
            dict[key] = '0'
        else:
            if isinstance(obj,decimal.Decimal):
                dict[key] = float('%0.4f'%dict[key])