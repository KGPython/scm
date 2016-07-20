# -*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base.utils import DateUtil,MethodUtil as mtu
from base.models import BasPurLog
import datetime,calendar,decimal
import xlwt3 as xlwt

@csrf_exempt
def index(request):
    monthFirst = datetime.date.today().replace(day=1)
    today = datetime.datetime.today()
    if(str(today)[8:10]=='01'):
        monthFirst = datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)
        today = datetime.date(datetime.date.today().year,datetime.date.today().month,1)-datetime.timedelta(1)
    todayStr = today.strftime('%y-%m-%d')
    monthFirstStr = str(monthFirst)

    conn = mtu.getMysqlConn()
    sqlTop= 'SElECT ShopID,shopname, SUM(qtyz) AS qtyzSum,SUM(qtyl) AS qtylSum,(sum(qtyl) / sum(qtyz)) AS zhonbiSum ' \
            'FROM KNegativestock ' \
            'WHERE sdate BETWEEN "'+monthFirstStr+'" AND "'+todayStr+'" GROUP BY ShopID ORDER BY ShopID'
    cur = conn.cursor()
    cur.execute(sqlTop)
    listTop= cur.fetchall()

    listTotal = {'ShopID': '合计', 'shopname': '', 'qtyzSum': 0}  # 初始化最后一行
    for i in range(0,len(listTop)):
        if(not listTop[i]['qtyzSum']):
            listTop[i]['qtyzSum']=0
        else:
            listTop[i]['qtyzSum'] = float(listTop[i]['qtyzSum'])
        if 'qtyzSum' in listTotal:
            listTotal['qtyzSum'] += listTop[i]['qtyzSum']
        else:
            listTotal['qtyzSum'] = listTop[i]['qtyzSum']

        if (not listTop[i]['qtylSum']):
            listTop[i]['qtylSum'] = 0
        else:
            listTop[i]['qtylSum'] = float(listTop[i]['qtylSum'])

        if 'qtylSum' in listTotal:
            listTotal['qtylSum'] += listTop[i]['qtylSum']
        else:
            listTotal['qtylSum'] = listTop[i]['qtylSum']

        if (not listTop[i]['zhonbiSum']):
            listTop[i]['zhonbiSum'] = 0
        else:
            listTop[i]['zhonbiSum'] = float('%0.2f' % (listTop[i]['zhonbiSum'] * 100))
        listTotal['zhonbiSum'] = listTotal['qtylSum'] / listTotal['qtyzSum']
        listTotal['zhonbiSum'] = str(float('%0.2f' % (listTotal['zhonbiSum'] * 100))) + '%'

        listTotal['mingciSum'] = ''

        sql = "SELECT b.sdate,SUM(b.qtyz) qtyz , SUM(b.qtyl) qtyl, (SUM(b.qtyl)/SUM(b.qtyz)) zhonbi, (SELECT COUNT(DISTINCT zhonbi) FROM KNegativestock a WHERE a.zhonbi <= b.zhonbi) AS mingci " \
              "FROM KNegativestock AS b " \
              "WHERE ShopID ='" + listTop[i]['ShopID'] + "' AND sdate BETWEEN '" + monthFirstStr + "' AND '" + todayStr + "' GROUP BY sdate"

        cur.execute(sql)
        listDetail = cur.fetchall()
        for item in listDetail:
            date = str(item['sdate'])[8:10]
            if(not item['qtyz']):
                listTop[i]['qtyz_'+date]=0
            else:
                listTop[i]['qtyz_' + date] = float(item['qtyz'])
            if 'qtyz_' + date in listTotal:
                listTotal['qtyz_' + date] += listTop[i]['qtyz_' + date]
            else:
                listTotal['qtyz_' + date] = listTop[i]['qtyz_' + date]

            if (not item['qtyl']):
                listTop[i]['qtyl_' + date] = 0
            else:
                listTop[i]['qtyl_' + date] = float(item['qtyl'])
            if 'qtyl_' + date in listTotal:
                listTotal['qtyl_' + date] += listTop[i]['qtyl_' + date]
            else:
                listTotal['qtyl_' + date] = listTop[i]['qtyl_' + date]

            if (not item['zhonbi']):
                listTop[i]['zhonbi_' + date] = 0
            else:
                listTop[i]['zhonbi_' + date] = float('%0.2f' % (item['zhonbi'] * 100))

            listTotal['zhonbi_' + date] = listTotal['qtyl_' + date] / listTotal['qtyz_' + date]
            listTotal['zhonbi_' + date] = str(float('%0.2f' % (listTotal['zhonbi_' + date] * 100))) + '%'

            listTotal['mingci_' + date] = ''
    TotalDict = {'listTotal':listTotal}
    listTop = ranking(listTop,'zhonbiSum','mingciSum')

    for date in range(1,today.day+1):
        if(date<10):
            listTop = ranking(listTop,'zhonbi_0'+str(date),'mingci_0'+str(date))
        else:
            listTop = ranking(listTop,'zhonbi_'+str(date),'mingci_'+str(date))
    listTop.sort(key=lambda x:x['ShopID'])

    ###课组汇总###
    yesterday = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%y-%m-%d %H:%M:%S')
    sqlDept = 'select deptid,deptidname,sum(qtyz) qtyz,sum(qtyl) qtyl,(sum(qtyl)/sum(qtyz)) zhonbi from KNegativestock' \
          ' where sdate="'+yesterday+'" group by deptid,deptidname order by deptid'
    cur = conn.cursor()
    cur.execute(sqlDept)
    listDept = cur.fetchall()
    for obj in listDept:
        if(not obj['qtyz']):
            obj['qtyz'] = 0
        obj['qtyz'] = float(obj['qtyz'])
        if(not obj['qtyl']):
            obj['qtyl'] = 0
        obj['qtyl'] = float(obj['qtyl'])
        if(not obj['zhonbi']):
            obj['zhonbi'] = 0
        obj['zhonbi'] = str(float('%0.4f'%obj['zhonbi'])*100)[0:4]+'%'

    ###负库存课组明细###
    sqlDeptDetail = 'SELECT shopid,shopname,deptid,deptidname,qtyz,qtyl,zhonbi FROM KNegativestock WHERE sdate = "'\
          +str(yesterday)+'" GROUP BY deptid,shopid'
    cur = conn.cursor()
    cur.execute(sqlDeptDetail)
    listDeptDetail = cur.fetchall()
    for obj in listDeptDetail:
        if(not obj['zhonbi']):
            obj['zhonbi']= 0
        obj['zhonbi'] = str(float('%0.4f'%obj['zhonbi'])*100)[0:4]+'%'
        if(not obj['qtyl']):
            obj['qtyl']= 0
        obj['qtyl'] = float(obj['qtyl'])
        if(not obj['qtyz']):
            obj['qtyz']= 0
        obj['qtyz'] = float(obj['qtyz'])
    cur.close()
    conn.close()

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
    BasPurLog.objects.create(name="超市负库存日报", url=path, qtype=qtype, ucode=ucode,uname=uname, createtime=today)

    if qtype== "1":
        return render(request,"report/daily/negative_stock_top.html",locals())
    else:
        return export(request,listTop,TotalDict,listDeptDetail,listDept)
def ranking(lis,key,name):
    lis.sort(key=lambda x:x[key])
    j = 1
    for i in range(0,len(lis)):
        if i > 0:
            a = lis[i-1]
            b = lis[i]
            if float(a[key]) != float(b[key]):
                j += 1
            b[name]= j
            a[key] = str(a[key])+'%'
        else:
            a = lis[i]
            a[name]= j
    return lis

def export(request,listTop,TotalDict,listDeptDetail,listDept):
    wb = xlwt.Workbook(encoding='utf-8',style_compression=0)
    #写入sheet1
    writeDataToSheet1(wb,listTop,TotalDict)
    #写入sheet2,sheet3
    writeDataToSheet2(wb,listDeptDetail,listDept)

    outtype = 'application/vnd.ms-excel;'
    fname = datetime.date.today().strftime("%m.%d")+"negative_daily_operate"
    response = mtu.getResponse(HttpResponse(),outtype,'%s.xls' % fname)
    wb.save(response)
    return response

def writeDataToSheet1(wb,listTop,TotalDict):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month
    lastDay = calendar.monthrange(year,month)[1]

    sheet = wb.add_sheet("（月）负库存排名日报",cell_overwrite_ok=True)

    titles = [[("（%s月）负库存排名日报" % month,0,1,15)],
              [("门店编号",0,2,1),("门店名称",1,2,1),("月累计排名(不含联营)",2,1,4)],
              [('有效商品数',2,1,1),('合计',3,1,1),('占比',4,1,1),('名次',5,1,1)]
              ]

    keylist = ['ShopID','shopname','qtyzSum','qtylSum','zhonbiSum','mingciSum']

    widthList = [600,1100,600,600,600,600]

    trow1 = titles[1]
    trow2 = titles[2]

    n = 6
    for d in range(1,lastDay+1):
        trow1.append((str(d)+'日排名(不含联营)',n,1,4))
        trow2.append(('有效商品数',n,1,1))
        trow2.append(('合计',n+1,1,1))
        trow2.append(('占比',n+2,1,1))
        trow2.append(('名次',n+3,1,1))
        widthList.append(600)
        widthList.append(400)
        widthList.append(400)
        widthList.append(400)
        n += 4
        if d<10:
            keylist.append('qtyz_0'+str(d))
            keylist.append('qtyl_0'+str(d))
            keylist.append('zhonbi_0'+str(d))
            keylist.append('mingci_0'+str(d))
        else:
            keylist.append('qtyz_'+str(d))
            keylist.append('qtyl_'+str(d))
            keylist.append('zhonbi_'+str(d))
            keylist.append('mingci_'+str(d))
    #日销售报表
    mtu.insertTitle2(sheet,titles,keylist,widthList)
    mtu.insertCell2(sheet,3,listTop,keylist,None)
    titlesLen = len(titles)
    listTopLen = len(listTop)
    mtu.insertSum2(sheet,keylist,titlesLen+listTopLen,TotalDict,2)

def writeDataToSheet2(wb,listDeptDetail,listDept):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month

    sheet2 = wb.add_sheet("（月）负库存课组明细日报",cell_overwrite_ok=True)
    sheet3 = wb.add_sheet("（月）负库存课组汇总日报",cell_overwrite_ok=True)

    titlesSheet2 = [[("（%s月）负库存课组明细日报" % month,0,1,7)],
              [("报表日期",3,1,1),("%s年-%s月-%s日"%(year,month,date.day),4,1,3)],
              [("门店编号",0,1,1),("门店名称",1,1,1),("课组编码",2,1,1),("课组名称",3,1,1),("课组汇总",4,1,1),("负库存数",3,1,1),("占比",3,1,1)]
              ]
    titlesSheet3 = [[("（%s月）负库存课组汇总日报" % month,0,1,5)],
              [("报表日期",2,1,1),("%s年-%s月-%s日"%(year,month,date.day),3,1,2)],
              [("课组编码",0,1,1),("课组名称",1,1,1),("课组汇总",2,1,1),("负库存数",3,1,1),("占比",4,1,1)]
              ]
    keylistSheet2 = ['shopid','shopname','deptid','deptidname','qtyz','qtyl','zhonbi']
    keylistSheet3 = ['deptid','deptidname','qtyz','qtyl','zhonbi']
    widthList = [600,1100,600,600,600,600]

    mtu.insertTitle2(sheet2,titlesSheet2,keylistSheet2,widthList)
    mtu.insertTitle2(sheet3,titlesSheet3,keylistSheet3,widthList)

    mtu.insertCell2(sheet2,3,listDeptDetail,keylistSheet2,None)
    mtu.insertCell2(sheet3,3,listDept,keylistSheet3,None)
