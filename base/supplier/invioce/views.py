# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from base.utils import MethodUtil,Constants
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
def createInvioce(request):
    suppCode = request.session.get('s_suppcode','100008')
    suppName = request.session.get('s_suppname','宽广主食厨房（05.08.80.85.86.87）')
    refSheetId = MethodUtil.getReqVal(request,'sheetid','CM01201412260144')
    conn2= MethodUtil.get_MssqlConn()

    #判断发票单据是否存在
    # sql = "select sheetid from CustReceive0 where venderid={venderid} and ShopID='CM01'".format(venderid=suppCode)
    # sheetList = conn2.execute_row(sql)

    #计划付款日期
    sql1 = "select c.TaxNo, a.PlanPayDate from billhead0 a, VenderCard b,VenderExt c where a.VenderID = b.VenderID and a.VenderID *= c.VenderID and  a.SheetID = '{sheetid}'".format(sheetid=refSheetId)
    dict1 = conn2.execute_row(sql1)
    PlanPayDate=dict1['PlanPayDate']
    sql3 = "select a.jsdate,a.flag,a.fnotes,b.taxno,c.paytypeid from vendercard a,venderext b,vender c	where a.venderid=b.venderid and a.venderid=c.venderid and a.venderid={venderid}".format(venderid=suppCode)
    dict3 = conn2.execute_row(sql3)

    sql2 = "select inshopid from billheaditem0 where sheetid ='{sheetid}'".format(sheetid=refSheetId)
    shopId = conn2.execute_row(sql2)['inshopid']
    timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render(request,'user_invoice.html',locals())


@csrf_exempt
def saveInvioce(request):
    conn = MethodUtil.getMssqlConn()
    conn2= MethodUtil.get_MssqlConn()
    suppCode = request.session.get('s_suppcode')
    suppName = request.session.get('s_suppname')

    ############接收表头相关数据（CustReceive0） ############
    planPayDate = request.POST.get('PlanPayDate')
    timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payDate =  request.POST.get('payDate',timeNow)
    shopId = request.POST.get('shopId')
    refSheetId = request.POST.get('refSheetId')

    #生成发票编号
    sqlSheetId = '''declare @i int,@SheetID char(16)
              exec @i=TL_GetNewSheetID 5204,@SheetID out
              select @SheetID
          '''
    sheetId = conn2.execute_scalar(sqlSheetId)

    if refSheetId:
        #结算起始时间、结束时间
        sqlDate = "select begindate,enddate from billhead0 where sheetid='{sheetid}'".format(sheetid=refSheetId)
        res1=conn2.execute_row(sqlDate)
        beginDate = res1['begindate'].strftime("%Y-%m-%d %H:%M:%S")
        endDate = res1['enddate'].strftime("%Y-%m-%d %H:%M:%S")

        sqlCR = "insert into CustReceive0 (SheetID, BillheadSheetID, VenderID, PlanPayDate, BeginDate, EndDate,Flag, Editor, EditDate, ShopID, Operator) " \
                "values('{sheetid}','{billheadsheetid}',{venderid},'{planpaydate}','{begindate}','{enddate}',{flag},'{editor}','{editdate}','{shopid}','' )"\
                .format(sheetid=sheetId,billheadsheetid=refSheetId,venderid=suppCode,planpaydate=planPayDate,begindate=beginDate,enddate=endDate,
                        flag=0,editor=suppCode,editdate=payDate,shopid='CM01')

    else:
        sqlCR = "insert into CustReceive0 (SheetID,VenderID, PlanPayDate,Flag, Editor, EditDate, ShopID, Operator) " \
                "values('{sheetid}',{venderid},'{planpaydate}',{flag},'{editor}','{editdate}','{shopid}','' )"\
                .format(sheetid=sheetId,venderid=suppCode,planpaydate=planPayDate,flag=0,editor=suppCode,editdate=payDate,shopid='CM01')

    ###########临时表相关过程(custitem0)############
    # sqlTemp0 = "drop table #Tempheaditem"
    # try:
    #     conn2.execute_non_query(sqlTemp0)
    # except Exception as e:
    #     print(e)
    sqlTemp1='''select b.paytypesortid,a.sheetid as refsheetid,a.sheettype as refsheettype,c.name sheetname, a.managedeptid,a.shopid as inshopid,
                 sum(costvalue) costvalue,sum(costvalue-costtaxvalue) notaxvalue,  sum(costtaxvalue) costtaxvalue,sum(salevalue) salevalue,a.agroflag,
                 a.payabledate,a.costtaxrate,a.shopid as fromshopid,a.invoicesheetid,0.00 as Dkrate,0 as BalanceBookSerialID
                 into #Tempheaditem
                 from unpaidsheet0 a,paytype b,serialnumber c  where a.paytypeid=b.id and a.sheettype*=c.serialid
                 and (a.costvalue<>0 or a.salevalue<>0) and a.sheetid is null
                 group by b.paytypesortid,a.sheetid,a.sheettype,c.name, a.managedeptid,a.shopid,a.agroflag,a.payabledate,a.costtaxrate,a.invoicesheetid
                 '''
    conn2.execute_non_query(sqlTemp1)
    sqlTemp2 = '''insert into #Tempheaditem (paytypesortid,refsheetid,refsheettype,sheetname,managedeptid, inshopid,costvalue,notaxvalue,costtaxvalue,
                    salevalue,agroflag,payabledate,costtaxrate,fromshopid,invoicesheetid,Dkrate,BalanceBookSerialID)
                    select b.paytypesortid,a.sheetid as refsheetid,a.sheettype as refsheettype,c.name sheetname, a.managedeptid,
                    a.shopid as inshopid,sum(costvalue) costvalue,sum(costvalue-costtaxvalue) notaxvalue,  sum(costtaxvalue) costtaxvalue,sum(salevalue) salevalue,
                    a.agroflag, a.payabledate,a.costtaxrate,a.shopid as fromshopid,a.invoicesheetid,0.00 as Dkrate,0
                    from unpaidsheet0 a,paytype b,serialnumber c
                    where  a.paytypeid=b.id and a.sheettype*=c.serialid and (a.costvalue<>0 or a.salevalue<>0)
                    and a.venderid in ( select venderid from vendercard where venderid={venderid}  or mastervenderid={venderid})
                    and a.BillHeadSheetID='{refsheetid}' and a.InvoiceSheetID is null
                    group by b.paytypesortid,a.sheetid,a.sheettype,c.name, a.managedeptid,a.shopid,a.agroflag,a.payabledate,a.costtaxrate,a.invoicesheetid
                    '''.format(refsheetid=refSheetId,venderid=suppCode)

    conn2.execute_non_query(sqlTemp2)
    sqlTemp3 = '''Insert into #Tempheaditem (paytypesortid,payabledate,refsheetid,refsheettype,sheetname,managedeptid, inshopid,costvalue,notaxvalue,costtaxvalue,
                salevalue,agroflag,costtaxrate,fromshopid,invoicesheetid,Dkrate,BalanceBookSerialID)
                select b.paytypesortid,Max(a.payabledate) payabledate,'',a.refsheettype,c.name,a.managedeptid, shopid,sum(costvalue),sum(costvalue-costtaxvalue),
                sum(costtaxvalue),sum(a.salevalue),a.agroflag,a.costtaxrate,a.fromshopid,a.invoicesheetid,0,a.serialid
                from balancebook0 a,paytype b,serialnumber c  where  a.refsheettype*=c.serialid and a.paytypeid=b.id
                and (a.costvalue<>0 or a.salevalue<>0)  and a.venderid in ( select venderid from vendercard where venderid={venderid}  or mastervenderid={venderid})
                and a.BillHeadSheetID='{refsheetid}' and a.InvoiceSheetID is null
                group by b.paytypesortid,a.refsheettype,c.name, a.managedeptid,a.shopid,a.agroflag,a.costtaxrate,a.fromshopid,a.invoicesheetid,a.serialid
                '''.format(refsheetid=refSheetId,venderid=suppCode)
    conn2.execute_non_query(sqlTemp3)
    sqlTemp4 = '''delete from #Tempheaditem where RefSheettype=2301 and CostValue = 0 '''
    conn2.execute_non_query(sqlTemp4)
    sqlTemp5 = '''select * from #tempheaditem'''
    conn2.execute_query(sqlTemp5)
    res2 = [ row for row in conn2 ]

    sqlTemp6 = '''drop table #tempheaditem'''
    conn2.execute_non_query(sqlTemp6)

    ############接收发票详细数据(CustReceiveItem0)############
    jsonStr = request.POST.get('jsonStr','')
    listData = json.loads(jsonStr)
    ############开始存储事务############
    res = {}
    conn.autocommit(False)
    cur = conn.cursor()
    try:
        #保存发票主要信息
        cur.execute(sqlCR)
        #保存custitem0表数据res2[i][12]
        for i in range(0,len(res2)):
            sqlCI = "insert into custitem0 " \
                    "values ('{SheetID}','{PayTypeSortID}','{PayableDate}','{RefSheetID}',{RefSheetType},{ManageDeptID},'{FromShopID}','{InShopID}','{CostValue}','{CostTaxValue}','{CostTaxRate}',{AgroFlag},'{SaleValue}',{BalanceBookSerialID})"\
                    .format(SheetID=sheetId,PayTypeSortID=res2[i][0],PayableDate=res2[i][11],RefSheetID=res2[i][1],RefSheetType=res2[i][2],ManageDeptID=res2[i][4],FromShopID=res2[i][13],InShopID=res2[i][5],
                            CostValue=res2[i][6],CostTaxValue=res2[i][8],CostTaxRate=res2[i][12],AgroFlag=res2[i][10],SaleValue=res2[i][9],BalanceBookSerialID=res2[i][16])
            cur.execute(sqlCI)
        #保存用户录入发票详细
        if listData:
            for data in listData:
                sqlCRI = "insert into CustReceiveItem0 values( '"+sheetId+"','"+data['cno']+"','"+suppName+"','"+data['cdno']+"','"+data['cdate']+"',"+data['cclass']+",'"+data['cgood']+"','"+data['ctaxrate']+"','"+data['cmoney']+"','"+data['csh']+"',"+data['paytype']+",'"+data['kmoney']+"','"+shopId+"')"
                cur.execute(sqlCRI)
            res['succ'] = True
        else:
            sql3 = "select a.jsdate,a.flag,a.fnotes,b.taxno,c.paytypeid from vendercard a,venderext b,vender c	where a.venderid=b.venderid and a.venderid=c.venderid and a.venderid={venderid}".format(venderid=suppCode)
            dict3 = conn2.execute_row(sql3)
            taxno = dict3["taxno"]
            sqlCRI = "insert into CustReceiveItem0 (sheetid,cno,cname,cdate,cclass,cgood,ctaxrate,cmoney,csh,cdno,PayType,kmoney,shopid) values( '"+sheetId+"','666666','"+suppName+"',getDate(),1,'货物',0.0,0.0,0.0,'"+taxno+"','1',0.0,'"+shopId+"')"
            cur.execute(sqlCRI)
            res['succ'] = True
    except Exception as e:
        print(e)
        res['succ'] = False
        conn.rollback()
    finally:
        conn.commit()

    sqlFlow = "insert into sheetflow(sheetid,sheettype,flag,operflag,checker,checkno,checkdate,checkdatetime) " \
              "values('{shid}',{shType},{flag},{operFlag},'{checker}',{chNo},convert(char(10),getdate(),120),getdate())"\
              .format(shid=sheetId,shType=res2[0][2],flag=0,operFlag=0,checker=suppCode,chNo=1)
    cur.execute(sqlFlow)
    print(sqlFlow)
    MethodUtil.insertSysLog(conn2,Constants.SCM_ACCOUNT_LOGINID,Constants.SCM_ACCOUNT_WORKSTATIONID,Constants.SCM_ACCOUNT_MODULEID,Constants.SCM_ACCOUNT_EVENTID[5],"操作员:{suppCode}保存单据[{sheetId}]".format(suppCode=suppCode,sheetId=sheetId))
    conn.commit()
    cur.close()
    conn.close()
    conn2.close()

    return HttpResponse(json.dumps(res))

def newInvoice(request):
    suppCode = request.session.get('s_suppcode')
    suppName = request.session.get('s_suppname')
    conn2= MethodUtil.get_MssqlConn()
    timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render(request,'user_invoice_new.html',locals())

@csrf_exempt
def queryBalance(request):
    suppCode = request.session.get('s_suppcode','100008')
    conn2 = MethodUtil.get_MssqlConn()
    refSheetId = request.POST.get('refSheetId','')
    payStatus = request.POST.get('payStatus','')
    queryDict={}
    if refSheetId:
        sql0 = "select sheetid from billhead0 where sheetid='{sheetid}'".format(sheetid=refSheetId)
        billhead0 = conn2.execute_scalar(sql0)
        if billhead0:
            #计划付款日期
            sql1 = "select c.TaxNo, a.PlanPayDate from billhead0 a, VenderCard b,VenderExt c where a.VenderID = b.VenderID and a.VenderID *= c.VenderID and  a.SheetID = '{sheetid}'".format(sheetid=refSheetId)
            dict1 = conn2.execute_row(sql1)
            if dict1:
                queryDict['PlanPayDate']=str(dict1['PlanPayDate'])

            sql3 = "select a.jsdate,a.flag,a.fnotes,b.taxno,c.paytypeid from vendercard a,venderext b,vender c	where a.venderid=b.venderid and a.venderid=c.venderid and a.venderid={venderid}".format(venderid=suppCode)
            dict3 = conn2.execute_row(sql3)
            if dict3:
                queryDict['payTypeId']=dict3['paytypeid']

            sql2 = "select inshopid from billheaditem0 where sheetid ='{sheetid}'".format(sheetid=refSheetId)
            shopId = conn2.execute_row(sql2)['inshopid']
            if shopId:
                queryDict['shopId']=shopId

            queryDict['succ']=True
        else:
            queryDict['succ']=False
    return HttpResponse(json.dumps(queryDict))