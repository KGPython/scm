# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from base.utils import MethodUtil,Constants
from django.shortcuts import render
from django.http import HttpResponse
from base.models import Billhead0,BasSupplier,Billheaditem0,Billhead0Status
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

@csrf_exempt
def createInvioce(request):
    suppCode = request.session.get('s_suppcode')
    suppName = request.session.get('s_suppname')
    refSheetId = MethodUtil.getReqVal(request,'sheetid')
    conn2= MethodUtil.get_MssqlConn()

    #判断发票单据是否存在
    # sql = "select sheetid from CustReceive0 where venderid={venderid} and ShopID='CM01'".format(venderid=suppCode)
    # sheetList = conn2.execute_row(sql)

    #计划付款日期
    balanceList = Billhead0.objects.filter(sheetid=refSheetId).values("planpaydate","begindate","enddate")
    if balanceList:
        balance=balanceList[0]
        PlanPayDate=balance['planpaydate']

        begindate = balance['begindate']
        enddate = balance['enddate']
    else:
        PlanPayDate = ''

    suppList = BasSupplier.objects.filter(suppcode=suppCode).values("taxno","paytypeid")
    if suppList:
        paytypeid = suppList[0]["paytypeid"]
        taxno = suppList[0]['taxno']
    else:
        paytypeid = ''

    itemList = Billheaditem0.objects.filter(sheetid=refSheetId).values("inshopid").order_by("inshopid")
    if itemList:
        shopId = itemList[0]['inshopid']
    else:
        shopId = ''

    timeNow = datetime.datetime.now().strftime("%Y-%m-%d")
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
    refSheetId = request.POST.get('refSheetId','')
    beginDate = request.POST.get("begindate",'')
    endDate = request.POST.get("enddate",'')
    jsonStr = request.POST.get('jsonStr','')

    res = {}
    sql="select top 1 SheetID from CustReceive0 where VenderID='{suppCode}' and flag=0".format(suppCode=suppCode)
    row = conn2.execute_row(sql)
    if row:
        res['succ']= '2'
        res['sheetid']= row["SheetID"]
    else:
        try:
            #生成发票编号
            sqlSheetId = '''declare @i int,@SheetID char(16)
                  exec @i=TL_GetNewSheetID 5204,@SheetID out
                  select @SheetID
              '''
            sheetId = conn2.execute_scalar(sqlSheetId)

            # ############开始存储事务############
            conn.autocommit(False)
            cur = conn.cursor()
            #保存发票主要信息
            sqlCR = "insert into CustReceive0 (SheetID, BillheadSheetID, VenderID, PlanPayDate, BeginDate, EndDate,Flag, Editor, EditDate, ShopID, Operator) " \
                "values('{sheetid}','{billheadsheetid}',{venderid},'{planpaydate}','{begindate}','{enddate}',{flag},'{editor}','{editdate}','{shopid}','' )" \
            .format(sheetid=sheetId,billheadsheetid=refSheetId,venderid=suppCode,planpaydate=planPayDate,begindate=beginDate,enddate=endDate,
                    flag=0,editor=suppCode,editdate=payDate,shopid='CM01')
            cur.execute(sqlCR)

            #保存custitem0表数据res2[i][12]
            res2 = findCustItem(conn2,refSheetId,suppCode)
            for i in range(0,len(res2)):
                sqlCI = "insert into custitem0 " \
                        "values ('{SheetID}','{PayTypeSortID}','{PayableDate}','{RefSheetID}',{RefSheetType},{ManageDeptID},'{FromShopID}','{InShopID}','{CostValue}','{CostTaxValue}','{CostTaxRate}',{AgroFlag},'{SaleValue}',{BalanceBookSerialID})" \
                    .format(SheetID=sheetId,PayTypeSortID=res2[i][0],PayableDate=res2[i][11],RefSheetID=res2[i][1],RefSheetType=res2[i][2],ManageDeptID=res2[i][4],FromShopID=res2[i][13],InShopID=res2[i][5],
                            CostValue=res2[i][6],CostTaxValue=res2[i][8],CostTaxRate=res2[i][12],AgroFlag=res2[i][10],SaleValue=res2[i][9],BalanceBookSerialID=res2[i][16])
                cur.execute(sqlCI)

            #保存用户录入发票详细
            listData = json.loads(jsonStr)
            if listData:
                for data in listData:
                    #kmoney默认为0无需录入
                    sqlCRI = "insert into CustReceiveItem0 values( '"+sheetId+"','"+data['cno']+"','"+suppName+"','"+data['cdno']+"','"+data['cdate']+"',"+data['cclass']+",'"+data['cgood']+"','"+data['ctaxrate']+"','"+data['cmoney']+"','"+data['csh']+"',"+data['paytype']+",'0.0','"+shopId+"')"
                    cur.execute(sqlCRI)
            else:
                sql3 = "select a.jsdate,a.flag,a.fnotes,b.taxno,c.paytypeid from vendercard a,venderext b,vender c	where a.venderid=b.venderid and a.venderid=c.venderid and a.venderid={venderid}".format(venderid=suppCode)
                dict3 = conn2.execute_row(sql3)
                taxno = dict3["taxno"]
                sqlCRI = "insert into CustReceiveItem0 (sheetid,cno,cname,cdate,cclass,cgood,ctaxrate,cmoney,csh,cdno,PayType,kmoney,shopid) values( '"+sheetId+"','666666','"+suppName+"',getDate(),1,'货物',0.0,0.0,0.0,'"+taxno+"','1',0.0,'"+shopId+"')"
                cur.execute(sqlCRI)

            sqlFlow = "insert into sheetflow(sheetid,sheettype,flag,operflag,checker,checkno,checkdate,checkdatetime) " \
                      "values('{shid}',{shType},{flag},{operFlag},'{checker}',{chNo},convert(char(10),getdate(),120),getdate())"\
                      .format(shid=sheetId,shType=5024,flag=0,operFlag=0,checker=Constants.SCM_ACCOUNT_LOGINID,chNo=Constants.SCM_ACCOUNT_LOGINNO)
            cur.execute(sqlFlow)

            conn.commit()

            #记录发票录入状态
            try:
                if refSheetId:
                    billhead = Billhead0.objects.values("sheetid","flag","editdate","grpcode","venderid","shopid").get(sheetid=refSheetId)
                    if billhead:
                        Billhead0Status.objects.create(sheetid=refSheetId,inviocestatus=1,flag=billhead["flag"],editdate=billhead["editdate"],grpcode=billhead["grpcode"],venderid=billhead["venderid"],shopid=billhead["shopid"])
            except Exception as e:
                print(e)

            res['succ'] = '0'

            MethodUtil.insertSysLog(conn2,Constants.SCM_ACCOUNT_LOGINID,Constants.SCM_ACCOUNT_WORKSTATIONID,Constants.SCM_ACCOUNT_MODULEID,Constants.SCM_ACCOUNT_EVENTID[5],"")
            MethodUtil.insertSysLog(conn2,Constants.SCM_ACCOUNT_LOGINID,Constants.SCM_ACCOUNT_WORKSTATIONID,Constants.SCM_ACCOUNT_MODULEID,Constants.SCM_ACCOUNT_EVENTID[6],"操作员:{suppCode}保存单据[{sheetId}]".format(suppCode=suppCode,sheetId=sheetId))
        except Exception as e:
            print(e)
            res['succ'] = '1'
            conn.rollback()
        finally:
            cur.close()
            conn.close()
            conn2.close()

    return HttpResponse(json.dumps(res))

def findCustItem(conn2,refSheetId,suppCode):
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
    return res2

def newInvoice(request):
    suppCode = request.session.get('s_suppcode')
    suppName = request.session.get('s_suppname')
    conn2= MethodUtil.get_MssqlConn()
    timeNow = datetime.datetime.now().strftime("%Y-%m-%d")
    suppList = BasSupplier.objects.filter(suppcode=suppCode).values("taxno","paytypeid")
    if suppList:
        paytypeid = suppList[0]["paytypeid"]
        taxno = suppList[0]['taxno']
    else:
        paytypeid = ''
        taxno = ''
    return render(request,'user_invoice_new.html',locals())

@csrf_exempt
def queryBalance(request):
    # suppCode = request.session.get('s_suppcode')
    # payStatus = request.POST.get('payStatus','')

    refSheetId = request.POST.get('refSheetId','')
    queryDict={}
    if refSheetId:
       try:
            conn2 = MethodUtil.get_MssqlConn()
            sql0 = "select sheetid,begindate,enddate,PlanPayDate from billhead0 where sheetid='{sheetid}'".format(sheetid=refSheetId.strip())
            billhead0 = conn2.execute_row(sql0)
            if billhead0:
                #计划付款日期
                # sql1 = "select c.TaxNo, a.PlanPayDate from billhead0 a, VenderCard b,VenderExt c where a.VenderID = b.VenderID and a.VenderID *= c.VenderID and  a.SheetID = '{sheetid}'".format(sheetid=refSheetId)
                # dict1 = conn2.execute_row(sql1)
                # if dict1:
                #     queryDict['PlanPayDate']=str(dict1['PlanPayDate'])

                # sql3 = "select a.jsdate,a.flag,a.fnotes,b.taxno,c.paytypeid from vendercard a,venderext b,vender c	where a.venderid=b.venderid and a.venderid=c.venderid and a.venderid={venderid}".format(venderid=suppCode)
                # dict3 = conn2.execute_row(sql3)
                # if dict3:
                #     queryDict['payTypeId']=dict3['paytypeid']

                sql2 = "select inshopid from billheaditem0 where sheetid ='{sheetid}'".format(sheetid=refSheetId)
                shopId = conn2.execute_row(sql2)['inshopid']
                if shopId:
                    queryDict['shopId']=shopId

                queryDict['PlanPayDate']=str(billhead0['PlanPayDate'])
                queryDict['begindate'] = str(billhead0["begindate"])
                queryDict['enddate'] = str(billhead0["enddate"])
                queryDict['succ']=True
            else:
                queryDict['succ']=False

       except Exception as e:
           print(e)
       finally:
           conn2.close()
    return HttpResponse(json.dumps(queryDict))