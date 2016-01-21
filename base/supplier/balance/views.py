# -*- coding:utf-8 -*-

import logging
import time,datetime,decimal,json
from .forms import *
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator  #分页查询

from base.models import Billhead0,Billheaditem0
from base.utils import MethodUtil as mtu,Constants

# Create your views here.
logger=logging.getLogger('base.supplier.stock.views')
time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
monthFrist = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")

#add by liubf at 2016/01/12
##编辑结算申请单
def applyEdit(request):
    venderid = request.session.get("s_suppcode")

    result = {}
    rdict = {}
    kxinvoice = decimal.Decimal(0)
    try:
        conn = mtu.get_MssqlConn()

        #查询供应商信息
        vender = findVender(conn,venderid)
        paytypeid = vender[0]
        # mastervid = vender[1]

        #g-购销 l-联营 d-代销  z-租赁
        contracttype = vender[4]
        pstart,pend,cstart,cend = getStartAndEndDate(contracttype)

        #供应商结算方式
        payTypeName = findPayTypeName(conn,paytypeid)

        #结算地
        balancePlace = findBalancePlace(conn)
        balancePlaceName = mtu.getDBVal(balancePlace,1)
        balancePlaceId = balancePlace[0]

        #上月销售信息
        #lastmonthsaleinfo = findLastMonthSaleInfo(conn,venderid)
        #上月销售金额
        #lastmonthsalevalue = lastmonthsaleinfo[0]
        #上月销售成本
        #lastmonthcostvalue = lastmonthsaleinfo[1]

        #查询单据信息（动态查询）
        rdict = findBillItem(conn,venderid,pstart,pend,cstart,cend)
        kxinvoice = findKxInvoice(conn,venderid,pend)
        kxinvoice = 300
        conn.close()

    except Exception as e:
        print(e)

    result["paytypeid"] = paytypeid   #结算方式ID
    result["payTypeName"] = payTypeName   #结算方式名称
    result["balancePlaceName"] = balancePlaceName     #结算地名称
    result["balancePlaceId"] = balancePlaceId         #结算地ID
    result["cstart"] = cstart
    result["cend"] = cend
    result["pstart"] = pstart
    result["pend"] = pend
    result["itemList"] = rdict["blist"]
    result["sum1"] = rdict["sum1"]
    result["sum2"] = rdict["sum2"]
    result["sum3"] = rdict["sum3"]
    result["sum4"] = rdict["sum4"]
    result["kxinvoice"] = kxinvoice
    result["zkinvoice"] = kxinvoice

    return render(request,"user_settleApply.html",result)

#保存结算申请单
@csrf_exempt
def applySave(request):
    s_ucode = request.session.get("s_ucode")
    venderid = request.session.get("s_suppcode")
    sheetId = mtu.getReqVal(request,"sheetId",None)
    pstart = mtu.getReqVal(request,"pstart",None)
    pend = mtu.getReqVal(request,"pend",None)
    cstart = mtu.getReqVal(request,"cstart",None)
    cend = mtu.getReqVal(request,"cend",None)
    refsheetids = mtu.getReqList(request,"refsheetid",None)
    # paytypeid = mtu.getReqVal(request,"paytypeid")
    # payTypeName = mtu.getReqVal(request,"payTypeName")
    balancePlaceId = mtu.getReqVal(request,"balancePlaceId")
    # balancePlaceName = mtu.getReqVal(request,"balancePlaceName")
    params = {}
    result = {}

    params["pstart"]=pstart
    params["pend"]=pend
    params["cstart"]=cstart
    params["cend"]=cend
    params["planpaydate"]=datetime.date.today().strftime("%Y-%m-%d")
    params["editor"]=s_ucode
    params["editdate"]=datetime.date.today().strftime("%Y-%m-%d")
    params["sheetid"] = sheetId
    params["venderid"] = venderid
    try:
        conn2 = mtu.get_MssqlConn()
        errors = 0
        try:
            rdict = findBillItem(conn2,venderid,pstart,pend,cstart,cend,refsheetids)
            if rdict:
                blist = rdict["blist"]
            else:
                blist = []

            payableamt = findPayableCostValue(conn2,balancePlaceId,venderid)
            if not payableamt:
                payableamt = decimal.Decimal(0.0)

            costvalue = findCostValue(conn2,venderid)
            if not costvalue:
                costvalue = decimal.Decimal(0.0)

            unjsvalue = unbalancedCostValue(conn2,venderid,pstart)
            if not unjsvalue:
                unjsvalue = decimal.Decimal(0.0)

            undqvalue = undueCostValue(conn2,venderid,pend)
            if not undqvalue:
                undqvalue = decimal.Decimal(0.0)

            advance = findAdvance(conn2,venderid)
            if not advance:
                advance = decimal.Decimal(0.0)

            payablemoney = sum([row["costvalue"] for row in blist])
            if not payablemoney:
                payablemoney = decimal.Decimal(0.0)

            params["payablemoney"]=float(payablemoney)   #应付金额
            params["advance"]=float(advance)        #预付款余额，预付款应扣金额(promoney)默认0 （写表billhead0）
            params["costvalue"]=float(costvalue)    #库存金额 （写表billhead0）
            params["undqvalue"]=float(undqvalue)    #未到期金额 （写表billhead0） 取不为空数据
            params["payableamt"]=float(payableamt)  #应付账款金额 （写表billhead0）
            params["unjsvalue"]=float(unjsvalue)    #应结未结金额 （写表billhead0） 取不为空数据

            conn = mtu.getMssqlConn()
            conn.autocommit(False)
            cursor = conn.cursor()

            klist = findKxsum(cursor,venderid,pend)
            kxmoney = sum([row["kmoney"] for row in klist])
            if not kxmoney:
                kxmoney = decimal.Decimal(0.0)

            cashlist = filter(lambda row:row["kkflag"]==0,[row for row in klist])
            invoicelist =  filter(lambda row:row["kkflag"]==1,[row for row in klist])

            kxcash = sum([row["kmoney"] for row in cashlist])
            if not kxcash:
                kxcash = decimal.Decimal(0.0)

            kxinvoice = sum([row["kmoney"] for row in invoicelist])
            if not kxinvoice:
                kxinvoice = decimal.Decimal(0.0)

            #应付金额=实付金额+帐扣金额
            #应开票金额=实付金额
            params["kxmoney"]=float(kxmoney)    #扣项金额合计
            params["kxcash"]=float(kxcash)      #扣项交款金额
            params["kxinvoice"]=float(kxinvoice)  #帐扣发票金额 (帐扣金额)

            if not sheetId:
                #新增
                type=0
                typeStr = "新增"
                sheetId = getSheetId(conn2)
                params["sheetid"] = sheetId
                saveBillHead0(cursor,params)
            else:
                #修改
                type = 1
                typeStr = "修改"
                updateBillHead0(cursor,params)

            #3.查询要保存的单据信息
            saveBillHeadItem(cursor,blist,sheetId)
            ##4 保存扣项明细
            saveKxItem(cursor,klist,sheetId)

            conn.commit()
        except Exception as e:
            errors += 1;
            conn.rollback()
            a,b = e.args
            print(a,str(b,"utf-8"))
        finally:
            cursor.close()
            conn.close()

        if errors <= 0:
            #执行保存存储过程
            sql = """declare @Result int
                   exec @Result=st_billheadsave '{sheetId}',{type},'{cname}','A001'
                   select @Result""".format(sheetId=sheetId,type=type,cname = Constants.SCM_ACCOUNT_USER_NAME)
            conn2.execute_scalar(sql)

            #保存日志记录
            note = "[SCM]操作员:[{operator}]{typeStr}单据[{sheetId}]".format(sheetId=sheetId,typeStr=typeStr,operator=s_ucode)
            mtu.insertSysLog(conn2,Constants.SCM_ACCOUNT_LOGINID,Constants.SCM_ACCOUNT_WORKSTATIONID,Constants.SCM_ACCOUNT_MODULEID,Constants.SCM_ACCOUNT_EVENTID[type],note)
            result["status"] = "0"
            result["sheetId"] = sheetId
        else:
            result["status"] = "1"
    except Exception as e:
        print(e)
    finally:
        conn2.close()

    #查询核算完后的数据
    # headList = findBillHead0(conn2,sheetId)
    # itemList = findBillHeadItem0(conn2,sheetId)

    # result["paytypeid"] = paytypeid   #结算方式ID
    # result["payTypeName"] = payTypeName   #结算方式名称
    # result["balancePlaceName"] = balancePlaceName     #结算地名称
    # result["balancePlaceId"] = balancePlaceId         #结算地ID
    # result["payablemoney"] = payablemoney     #应付金额
    # result["kxinvoice"] = kxinvoice         #帐扣金额
    # result["paidmoney"] = payablemoney - kxinvoice    #实付金额
    # result["zkinvoice"] = payablemoney - kxinvoice    #帐扣可充发票
    #
    # result["pstart"]=pstart
    # result["pend"]=pend
    # result["cstart"]=cstart
    # result["cend"]=cend
    # result["sheetId"] = sheetId
    # result["itemList"] = blist
    return HttpResponse(json.dumps(result))

# def findBillHead0(conn2,sheetid):
#     ##表头
#     sql = """select a.*,b.vendername as spname,b.kkflag,b.fkflag venderfkflag  ,
#               d.Name,d.TaxRate,s.Address,s.LinkTele,s.TaxNo,s.KHBank,s.AccNo
#               from billhead0 a,VenderCard b,VenderExt c,TaxPayer d,shop s
#               where a.InvoiceShopID*=s.ID and a.venderid=b.venderid and a.flag=0
#               and dbo.FunUserShopVenderPower(1,'8935',a.shopid,'',0)=1
#               and a.VenderID=c.VenderID and c.TaxPayerID=d.ID
#               and (sheetid='{sheetid}')  order by a.sheetid desc
#             """.format(sheetid=sheetid)
#     conn2.execute_query(sql)
#     return [row for row in conn2]
#
# def findBillHeadItem0(conn2,sheetid):
#
#     sql = """select distinct a.SheetID,a.PayTypeSortID,a.PayableDate,a.RefSheetID,a.RefSheetType,a.ManageDeptID,
#                 a.FromShopID,a.InShopID,a.CostValue,a.CostTaxValue,a.CostTaxRate,a.AgroFlag,a.SaleValue,a.InvoiceSheetID,
#                 a.DKRate,a.SerialID,b.name as sheetname,(a.CostValue-a.CostTaxValue) NoTaxValue,c.refsheetid as Adjustsheetid,
#                 c.refsheettype as Adjustsheettype,d.name as Adjustsheetname,1 as checkFlag , e.name as inshopname,
#                 isnull(f.CheckDate,g.CheckDate) CheckDate from billheaditem0 a
#                 left join serialnumber b on  a.refsheettype = b.serialid
#                 left join UpdPayableTemp c on c.sheetid = a.refsheetid and a.refsheettype = 5205
#                 left join serialnumber d on  c.refsheettype = d.serialid
#                 left join shop e on a.inshopid = e.id
#                 left join UnpaidSheet0 f on a.sheetid = f.BillheadSheetID and a.RefSheetType = f.SheetType and a.refsheetid = f.SheetID
#                 left join UnpaidSheet g on a.sheetid = g.BillheadSheetID and a.RefSheetType = g.SheetType and a.refsheetid = g.SheetID
#                 where a.sheetid='{sheetid}'
#             """.format(sheetid=sheetid)
#     conn2.execute_query(sql)
#     return [row for row in conn2]

def getSheetId(conn):
    #1.取单据号
    sql = """declare @i int,@SheetID char(16)
           exec @i=TL_GetNewSheetID 5203,@SheetID out
           select @SheetID"""
    sheetId = conn.execute_scalar(sql)
    return sheetId

def findKxInvoice(conn,venderid,pend):
    sql = """select ISNULL(sum(a.kmoney),0) from kxsum0 a
                 where a.venderid in ( select venderid from vendercard where venderid={venderid}  or mastervenderid={venderid})
                 and a.flag=0 and a.stoppay=0 and a.kkflag = 1
                 and ( (a.ktype=1 and ReceivableDate<='{pend}') or (a.ktype=0 and a.style<>0 ))
                 """.format(venderid=venderid,pend=pend)
    sum = conn.execute_scalar(sql)
    return sum

#取费用数据 (次表体)（写表billheadkxitem0）
def findKxsum(cursor,venderid,pend):
    sql = """select a.SerialID,a.shopid as inshopid,a.managedeptid,a.kno,b.kname,a.ktype,a.kmoney,a.kkflag, a.style,a.monthid,
                 a.receivabledate,a.note,a.fromshopid,b.prtflag, c.name as inshopname
                 from kxsum0 a, kxd b  , shop c where a.venderid in
                 ( select venderid from vendercard where venderid={venderid}  or mastervenderid={venderid})
                 and a.flag=0 and a.stoppay=0 and a.shopid *= c.id
                 and  a.kno = b.kno and ( (a.ktype=1 and ReceivableDate<='{pend}') or (a.ktype=0 and a.style<>0 ))
                 order by a.kno
                 """.format(venderid=venderid,pend=pend)
    cursor.execute(sql)
    rlist = cursor.fetchall()
    return rlist

#保存扣项费用信息
def saveKxItem(cursor,rlist,sheetid):
    ##删除扣项费用信息
    sql = "delete from billheadkxitem0 where SheetID='{sheetId}'".format(sheetId=sheetid)
    cursor.execute(sql)

    for row in rlist:
        sql = """ insert into billheadkxitem0
                 (SerialID,          --1扣项序号
                  SheetID,           --2付款单号
                  kno,               --3扣项代码
                  Ktype,             --4扣项类型　0-固定 1-临时
                  PayableDate,       --5应收日期
                  FromShopID,        --6来源地（代销显示直通/配送金额）
                  InShopID,          --7发生地商场号
                  ManageDeptID,      --8管理部类
                  kmoney,            --9扣款金额
                  kkflag,            --10扣项交款方式，0=交款 1=扣款(从货款中扣) 2=供应商默认方式
                  Style,             --11计算方法 0=按结算单收取 1=按月收取 2=按年收取
                  MonthID,           --12年月(YYYYMM),计算方法等于1,2时写入
                  ReceiptID,         --13收据号,打印收据时使用,生成的收据号保存到Receipt表中
                  note               --14扣款备注
                  )
                values({serialid},'{sheetid}',{kno},{ktype},'{payabledate}','{fromshopid}','{inshopid}',
                {managedeptid},{kmoney},{kkflag},{style},{monthid},NULL,'{note}')
                """.format(serialid=row["SerialID"],sheetid=sheetid,kno=row["kno"],ktype=row["ktype"],
                           payabledate=row["receivabledate"],fromshopid=row["fromshopid"],inshopid=row["inshopid"],
                           managedeptid=row["managedeptid"],kmoney=float(row["kmoney"]),kkflag=row["kkflag"],
                           style=row["style"],monthid=row["monthid"],note=mtu.getDBVal(row,"note"))
        cursor.execute(sql)

def saveBillHead0(cursor,params):

     sql = """insert into billhead0
                     (SheetID,            --1单号
                      ShopID,             --2分店号,只能是区域中心 CM01
                      VenderID,           --3供应商编码
                      PayableMoney,       --4本期应付金额(sum billheaditem0.costvalue)
                      KXMoney,            --5本期扣项金额合计(sum billheadkxitem0.kxmoney)
                      KXCash,             --6本期扣项交款金额
                      KXInVoice,          --7本期帐扣发票金额
                      PayableAmt,         --8本期供应商应付帐款
                      CloseValue,         --9本期供应商库存金额
                      unjsvalue,          --10应该结未结金额
                      undqvalue,          --11未到期结算金额
                      HavInVoice,         --12是否有发票号码 0-没有发票 1-有发票
                      Flag,               --13标志 0-制单 1-制单审核 2-付款审核 3-缴款审核 100-确认
                      PayType,            --14  1=支票 2=电汇 3=汇票 0=其他
                      BeginDate,          --15结算开始日期
                      EndDate,            --16结算结束日期
                      PlanPayDate,        --17计划付款日期
                      Editor,             --18制单人
                      EditDate,           --19制单日期
                      Operator,           --20业务员
                      Checker,            --21制单审核人，一旦确认后，不可再修改
                      CheckDate,          --22制单审核日期
                      PayChecker,         --23付款审批人，付款确认人可以取消该单
                      PayCheckDate,       --24付款审批日期
                      Receiver,           --25出纳，当供应商扣项缴现金时，出纳签字
                      ReceivDate,         --26出纳收款日期
                      Payer,              --27财务付款人
                      PayDate,            --28财务付款日期
                      PayAmt,             --29  '0'
                      PayTaxAmt17,        --30  '0'
                      PayTaxAmt13,        --31  '0'
                      PayTaxAmt6,         --32  '0'
                      PayTaxAmt4,         --33  '0'
                      PrintCount,         --34打印次数
                      FPrintCount,        --35付款通知书中加入打印次数打印次数
                      Note,               --36备注
                      OpenMoney,          --37上期余额
                      CloseMoney,         --38转下期应付
                      PreMoney,           --39预付款应扣金额
                      InvoiceShopID,      --40商场门店
                      BeginSDate,         --41单据开始日期
                      EndSDate,           --42单据结束日期
                      CurDXValue,         --43本期代销勾单金额
                      CurDXDiffValue,     --44本期代销勾单差额
                      LastDXDiffValue,    --45上期代销勾单差额
                      NotDXFlag,          --46本次不勾单标志 0=勾单 1=不勾单
                      Advance,            --47预付款余额
                      Accounter,          --48 null
                      AccountDate         --49 null
                      )values('{sheetid}','{shopid}',{venderid},{payablemoney},{kxmoney},{kxcash},{kxinvoice},{payableamt},{costvalue},{unjsvalue},
                       {undqvalue},0,0,1,'{pstart}', '{pend}','{planpaydate}','{editor}','{editdate}','{operator}',NULL,NULL,NULL,NULL,NULL,NULL,
                       NULL,NULL, 0.0,0.0,0.0,0.0,0.0,0,0,NULL,0,0,0,NULL,'{cstart}','{cend}',0,0,0,0,{advance},NULL,NULL)
            """.format(sheetid=params["sheetid"],shopid="CM01",venderid=params["venderid"],payablemoney=params["payablemoney"],
                       kxmoney=params["kxmoney"],kxcash=params["kxcash"], kxinvoice=params["kxinvoice"],payableamt=params["payableamt"],
                       costvalue=params["costvalue"],unjsvalue=params["unjsvalue"],undqvalue=params["undqvalue"],pstart=params["pstart"],
                       pend=params["pend"],planpaydate=params["planpaydate"],editor=params["editor"],editdate=params["editdate"],
                       operator=params["editor"],cstart=params["cstart"],cend=params["cend"],advance=params["advance"])
     cursor.execute(sql)

def updateBillHead0(cursor,params):
     sql = """update billhead0 set
                      PayableMoney={payablemoney}, --4本期应付金额(sum billheaditem0.costvalue)
                      KXMoney={kxmoney},           --5本期扣项金额合计(sum billheadkxitem0.kxmoney)
                      KXCash={kxcash},             --6本期扣项交款金额
                      KXInVoice={kxinvoice},       --7本期帐扣发票金额
                      PayableAmt={payableamt},     --8本期供应商应付帐款
                      CloseValue={costvalue},      --9本期供应商库存金额
                      unjsvalue={unjsvalue},       --10应该结未结金额
                      undqvalue={undqvalue},       --11未到期结算金额
                      Advance={advance}            --47预付款余额
                      where SheetID='{sheetid}'
            """.format(sheetid=params["sheetid"],payablemoney=params["payablemoney"], kxmoney=params["kxmoney"],kxcash=params["kxcash"],
                       kxinvoice=params["kxinvoice"],payableamt=params["payableamt"],costvalue=params["costvalue"],unjsvalue=params["unjsvalue"],
                       undqvalue=params["undqvalue"],advance=params["advance"])
     cursor.execute(sql)


def saveBillHeadItem(cursor,dlist,sheetId):
    #删除单据明细
    sql = "delete from billheaditem0 where SheetID='{sheetId}'".format(sheetId=sheetId)
    cursor.execute(sql)

    for row in dlist:
        paytypesortid = row["paytypesortid"]
        if paytypesortid not in ["g","d"]:
            paytypesortid = "d"
        #保存单据明细
        sql = """insert into billheaditem0
                 (SheetID,         --1付款通知单号
                  PayTypeSortID,   --2结算类型 g=购销 d=代销 d=其他
                  PayableDate,     --3应付日期
                  RefSheetID,      --4相关单号
                  RefSheetType,    --5单据类型
                  ManageDeptID,    --6管理部类
                  FromShopID,      --7来源地（代销显示直通/配送金额）
                  InShopID,        --8发生地商场号（代销显示各店应结明细/或不区分）
                  CostValue,       --9应结金额（含税）
                  CostTaxValue,    --10税金
                  CostTaxRate,     --11进项税率
                  AgroFlag,        --12免税农产品标志(0=不是 1=是)
                  SaleValue,       --13销售金额
                  InvoiceSheetID,  --14发票接收单号
                  DKRate           --15倒扣率
                  )values('{sheetid}','{paytypesortid}','{payabledate}','{refsheetid}',{refsheettype},{managedeptid},'{fromshopid}','{inshopid}',{costvalue},
                   {costtaxvalue},{costtaxrate},{agroflag},{salevalue},'{invoicesheetid}','{dkrate}')
                  """.format(sheetid=sheetId,paytypesortid=paytypesortid,payabledate=row["payabledate"],refsheetid=row["refsheetid"],
                             refsheettype=row["refsheettype"],managedeptid=row["managedeptid"],fromshopid=row["fromshopid"],inshopid=row["inshopid"],
                             costvalue=float(row["costvalue"]),costtaxvalue=float(row["costtaxvalue"]),costtaxrate=float(row["costtaxrate"]),
                             agroflag=row["agroflag"],salevalue=float(row["salevalue"]),invoicesheetid=row["invoicesheetid"],dkrate=row["Dkrate"])
        cursor.execute(sql)

#根据经营方式获得结算日期、单据日期
def getStartAndEndDate(contracttype):
    stime = Constants.ERP_START_TIME

    #结算日期
    #erp系统使用的开始时间
    pstart = datetime.date(stime[0],stime[1],stime[2]).strftime("%Y-%m-%d")
    #当前日期
    pend = datetime.datetime.now().strftime("%Y-%m-%d")
    if contracttype=="g":   #购销
        #单据日期
        cstart = datetime.date(stime[0],stime[1],stime[2]).strftime("%Y-%m-%d")
        cend = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        #单据日期 上月一整月
        cstart = (datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=1).strftime("%Y-%m-%d")
        cstart = "2012-01-01"
        cend = (datetime.date.today().replace(day=1) - datetime.timedelta(1)).strftime("%Y-%m-%d")
    return pstart,pend,cstart,cend


def findVender(conn,venderid):
     sql = "select paytypeid,MasterVenderID,clearflag,name,ContractType,ifdxgd from vender where venderid={venderid}".format(venderid=venderid)
     return conn.execute_row(sql)

def findPayTypeName(conn,paytypeid):
    sql = "select id+'| '+name as name,runType from paytype where id={paytypeid}".format(paytypeid=paytypeid)
    rs = conn.execute_row(sql)
    payTypeName = mtu.getDBVal(rs,0)
    return payTypeName

def findBalancePlace(conn):
    sql = "SELECT a.id,a.name from shop a,config b where a.id=b.value and b.name='本店号'"
    rs = conn.execute_row(sql)
    return rs

def findPayableCostValue(conn,balanceId,venderid):
   sql = """
        declare @shopid char(4),@vendreid int ,@payvalue dec(12,2)
        exec TL_venderpayable  {balanceId},{venderid},@payvalue
        output  select @payvalue""".format(balanceId=balanceId,venderid=venderid)
   payvalue = conn.execute_scalar(sql)  #获得一个返回参数
   return payvalue
#
# def findLastMonthSaleInfo(conn,venderid):
#     lastMonth =(datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=1).strftime("%Y%m")
#     sql = """select sum(SaleValue),sum(costvalue) from RPT_PaymentNote
#                   where monthid={lastMonth} and venderid={venderid}""".format(lastMonth=lastMonth,venderid=venderid)
#     rs = conn.execute_row(sql)
#     return rs

def findCostValue(conn,venderid):
    sql = """
       if object_id('tempdb..#520311Vender') is not null
            drop table #520311Vender
       create table #520311Vender(
            VenderID int not null,
            primary key (venderID)
       );"""
    conn.execute_non_query(sql)

    sql = """insert into #520311Vender select distinct VenderID from VenderCard
              where VenderID={venderid} Or MasterVenderID={mastervenderid}""".format(venderid=venderid,mastervenderid=venderid)
    conn.execute_non_query(sql)

    sql = """
        if object_id('tempdb..#520311Cost') is not null
            drop table #520311Cost
        create table #520311Cost(
            GoodsID int not null,
            ShopId	char(4) not null,
            VenderID int not null,
            primary key (GoodsID,ShopID,VenderID)
        ); """
    conn.execute_non_query(sql)

    sql = """insert into #520311Cost select GoodsID,ShopID,VenderID from Cost where VenderID in (select VenderID from #520311Vender)"""
    conn.execute_non_query(sql)

    #库存金额
    sql = """
         select sum(a.costvalue)  from shopsstock a,cost b,goods c
         where a.goodsid=b.goodsid  and a.shopid=b.shopid and b.flag=0 and a.goodsid=c.goodsid
         and c.stocktype=2 and b.venderid  in (select venderid from #520311Vender)
       """
    costvalue = conn.execute_scalar(sql)

    #删除临时表
    sql = """
        if object_id('tempdb..#520311Vender') is not null drop table #520311Vender
        if object_id('tempdb..#520311Cost') is not null drop table #520311Cost
        """
    conn.execute_non_query(sql)
    return costvalue

def unbalancedCostValue(conn,venderid,payabledate):
    sql = """select sum(costvalue)  from balancebook0 a,paytype b
                  where  a.payabledate <'{payabledate}' and  a.paytypeid=b.id and a.payflag=0 and a.venderid={venderid}""".format(venderid=venderid,payabledate=payabledate)
    item = conn.execute_row(sql)
    costvalue = item[0]
    if not costvalue:
         sql = """select sum(costvalue) costvalue  from unpaidsheet0 a,paytype b  where  a.venderid = {venderid} and a.payabledate <'{payabledate}' and
                     a.paytypeid=b.id and (a.costvalue<>0 or a.salevalue<>0) and a.payflag=0""".format(venderid=venderid,payabledate=payabledate)
         item = conn.execute_row(sql)
         costvalue = item[0]
    return costvalue

def undueCostValue(conn,venderid,payabledate):
    sql = """select sum(costvalue)  from balancebook0 a,paytype b where  a.payabledate >'{payabledate}' and  a.paytypeid=b.id
                  and a.payflag=0 and a.venderid={venderid}""".format(venderid=venderid,payabledate=payabledate)
    item = conn.execute_row(sql)
    costvalue = item[0]
    if not costvalue:
        sql = """select sum(costvalue) costvalue  from unpaidsheet0 a,paytype b  where  a.venderid = {venderid} and a.payabledate >'{payabledate}' and
                      a.paytypeid=b.id and (a.costvalue<>0 or a.salevalue<>0) and a.payflag=0""".format(venderid=venderid,payabledate=payabledate)
        item = conn.execute_row(sql)
        costvalue = item[0]
    return costvalue

def findAdvance(conn,venderid):
    sql = "select ShopID,VenderID,PreMoney,AccFlag,sDate,BillheadSheetID from PreMoney where venderid='{venderid}'".format(venderid=venderid)
    item = conn.execute_row(sql)
    return item


def findBillItem(conn,venderid,pstart,pend,cstart,cend,refsheetidList=None):
    #创建结算明细
    createTempheaditemTable(conn)

    #1.插入单据数据:验收单、退货单、往来单据调整单
    for i in range(1,5):
        insertBillSheet(conn,venderid,pstart,pend,cstart,cend,i)

    #5.联营\代销结算流水  101=销售流水\ 102=分摊流水 \104=促销折扣流水\2413=报损单\2423=行政领用单\2451=批发通知单/批发单
    insertAssociatedToTempheaditem(conn,venderid,pstart,pend,cstart,cend)

    #6.删除赠品入库
    deleteGiftInStorage(conn)

    #7.查询单据明细
    rdict = findBillItemList(conn,refsheetidList)

    return rdict

#创建临时表存储待结算单据信息
def createTempheaditemTable(conn):
    sql = """
        if object_id('tempdb..#Tempheaditem') is not null
                 drop table #Tempheaditem ;
        create table #Tempheaditem(
             paytypesortid varchar(1)  not null ,
             payabledate  datetime ,
             refsheetid varchar(16) ,
             refsheettype int ,
             sheetname varchar(50) not null ,
             managedeptid int not null ,
             inshopid char(4) ,
             costvalue dec(12,2)	not null ,
             notaxvalue dec(12,2)  not null ,
             costtaxvalue dec(12,2) not null ,
             salevalue dec(12,2) ,
             agroflag int ,
             costtaxrate dec(4,2) not null ,
             fromshopid varchar(4) ,
             invoicesheetid varchar(16) ,
             Dkrate dec(5,2) not null default 0
        )
        create index tempheaditem_index on #Tempheaditem(InShopID,refsheetid);
        """
    conn.execute_non_query(sql)

#查询验收单
def insertBillSheet(conn,venderid,pstart,pend,cstart,cend,type):

    condition = "and 1=1 "
    if type==1:      #1.验收单据
        condition = """and convert(char(8),a.payabledate,112)  between '{pstart}' and '{pend}'
                    and convert(char(8),a.CheckDate,112) between '{cstart}' and '{cend}'
                    and  a.sheettype<>2323 and a.sheettype<>5205
                    """.format(pstart=pstart,pend=pend,cstart=cstart,cend=cend)
    elif type==2:    #2.退货单
        condition = """and  convert(char(8),a.payabledate,112)<= '{pend}'
                    and  convert(char(8),a.CheckDate,112)<= '{cend}'
                    and  a.sheettype=2323
                    """.format(pend=pend,cend=cend)
    elif type==3:    #3.供应商往来单据金额调整单  单据金额>=0
        condition = """and convert(char(8),a.payabledate,112)  between '{pstart}' and '{pend}'
                    and convert(char(8),a.CheckDate,112) between '{cstart}' and '{cend}'
                    and  a.sheettype=5205 and a.costvalue > 0
                    """.format(pstart=pstart,pend=pend,cstart=cstart,cend=cend)
    elif type==4:    #4.供应商往来单据金额调整单  单据金额<=0
        condition = """and  a.sheettype=5205 and a.costvalue <= 0  """

    sql = """
            insert into #Tempheaditem(paytypesortid,refsheetid,refsheettype,sheetname,managedeptid, inshopid,costvalue,
            notaxvalue,costtaxvalue,salevalue,agroflag,payabledate,costtaxrate,fromshopid,invoicesheetid,DKrate)
           select b.paytypesortid,a.sheetid as refsheetid,a.sheettype as refsheettype,c.name sheetname,
               a.managedeptid,a.shopid as inshopid,sum(costvalue) costvalue,sum(costvalue-costtaxvalue) notaxvalue,
               sum(costtaxvalue) costtaxvalue,sum(salevalue) salevalue,a.agroflag, a.payabledate,a.costtaxrate,
               a.shopid as fromshopid,IsnuLL(a.invoicesheetid,'') as invoicesheetid,0
           from unpaidsheet0 a,paytype b,serialnumber c
           where  a.venderid in ( select venderid from vendercard where venderid={venderid}  or mastervenderid={venderid})
            {condition}
            and a.paytypeid=b.id and a.sheettype*=c.serialid
            and (a.costvalue<>0 or a.salevalue<>0) and a.payflag=0
            group by b.paytypesortid,a.sheetid,a.sheettype,c.name,
            a.managedeptid,a.shopid,a.agroflag,a.payabledate,a.costtaxrate,a.invoicesheetid
            order by sheettype,payabledate,sheetid
            """.format(venderid=venderid,condition=condition)
    conn.execute_non_query(sql)

#查询联营\代销结算流水  101=销售流水\ 102=分摊流水 \104=促销折扣流水\2413=报损单\2423=行政领用单\2451=批发通知单/批发单
def insertAssociatedToTempheaditem(conn,venderid,pstart,pend,cstart,cend):
    sql = """insert into #Tempheaditem
             (paytypesortid,payabledate,refsheetid,refsheettype,sheetname,managedeptid, inshopid,costvalue,notaxvalue,costtaxvalue,
             salevalue,agroflag,costtaxrate,fromshopid,invoicesheetid,Dkrate)
             select b.paytypesortid,Max(a.payabledate) payabledate,''  ,a.refsheettype,c.name,a.managedeptid, shopid,sum(costvalue) costvalue,
             sum(costvalue-costtaxvalue) notaxvalue, sum(costtaxvalue), sum(a.salevalue),a.agroflag,a.costtaxrate,a.fromshopid,
             isnull(a.invoicesheetid,''),isnull(a.Dkrate,0) as DkRate
             from balancebook0 a,paytype b,serialnumber c
             where  a.refsheettype*=c.serialid  and convert(char(8),a.payabledate,112) between '{pstart}' and '{pend}'
             and convert(char(8),a.SDate,112) between '{cstart}' and '{cend}' and a.paytypeid=b.id and a.payflag=0
             and a.venderid in ( select venderid from vendercard where venderid={venderid}  or mastervenderid={venderid})
             group by b.paytypesortid,a.refsheettype,c.name,a.managedeptid,a.shopid,a.agroflag,a.costtaxrate,a.fromshopid,a.invoicesheetid,a.Dkrate
             order by shopid,PayableDate
            """.format(venderid=venderid,pstart=pstart,pend=pend,cstart=cstart,cend=cend)
    conn.execute_non_query(sql)

#删除赠品入库
def deleteGiftInStorage(conn):
    sql = """ delete from #Tempheaditem where RefSheettype=2301 and CostValue = 0 """
    conn.execute_non_query(sql)

#查询单据明细
def findBillItemList(conn,refsheetidList=None):
    condition = "where {cond1}"
    cond1 = "1=1"
    if refsheetidList:
        sids = "','".join(refsheetidList)
        cond1 = "a.refsheetid in ('{sids}')".format(sids=sids)

    condition = condition.format(cond1=cond1)

    sql = """select a.paytypesortid ,a.payabledate,a.refsheetid,a.refsheettype,a.sheetname,a.managedeptid,a.inshopid,a.costvalue,
              a.notaxvalue,a.costtaxvalue,a.salevalue,a.agroflag,a.costtaxrate,a.fromshopid,a.invoicesheetid,a.Dkrate,
              c.refsheetid as Adjustsheetid, c.refsheettype as Adjustsheettype,d.name as Adjustsheetname, e.name as inshopname
              from #tempheaditem  a
              left join UpdPayableTemp c on c.sheetid = a.refsheetid and a.refsheettype = 5205
              left join serialnumber d on  c.refsheettype = d.serialid
              left join shop e on a.inshopid = e.id
              {condition}
              order by a.InShopID,a.refsheetid""".format(condition=condition)
    conn.execute_query(sql)

    rs = {}
    blist = []
    sum1 = decimal.Decimal(0.0)
    sum2 = decimal.Decimal(0.0)
    sum3 = decimal.Decimal(0.0)
    sum4 = decimal.Decimal(0.0)
    for row in conn:
        blist.append(row)
        sum1 += row["costvalue"]
        sum2 += row["notaxvalue"]
        sum3 += row["costtaxvalue"]
        sum4 += row["salevalue"]

    rs["blist"] = blist
    rs["sum1"] = sum1
    rs["sum2"] = sum2
    rs["sum3"] = sum3
    rs["sum4"] = sum4

    return rs

#end by liubf at 2016/01/12

def balance(request):
    sperCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    start = monthFrist
    end = time
    shopId = []
    sheetId = ''
    status = ''
    orderStyle = '-editdate'
    page = request.GET.get('page',1)
    if request.method== 'POST':
        form = BillInForm(request.POST)
        if form.is_valid():
            shopId = form.cleaned_data['shopid']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            sheetId = form.cleaned_data['sheetId']
            status = form.cleaned_data['status']
            orderStyle = form.cleaned_data['orderStyle']
    else:
        shopId = request.GET.get('shopcode','')
        start = request.GET.get('start',monthFrist)
        end = request.GET.get('end',time)
        sheetId = request.GET.get('sheetid','')
        status = request.GET.get('status','')
        orderStyle = request.GET.get('orderstyle','editdate')
        data = {'shopid':shopId,'start':start,'end':end,'sheetId':sheetId,'status':status}
        form = BillInForm(data)

    kwargs = {}
    if status:
        kwargs.setdefault('status__contains',status)
    if sheetId:
        kwargs.setdefault('sheetid__contains',sheetId)
    if len(shopId):
        shopId = shopId[0:(len(shopId)-1)]
        shopId =shopId.split(',')
        kwargs.setdefault('shopid__in',shopId)
    kwargs.setdefault('editdate__gte',start)
    kwargs.setdefault('editdate__lte',end)
    kwargs.setdefault('venderid',sperCode)
    kwargs.setdefault('grpcode',grpCode)

    balanceList = Billhead0.objects.values("shopid","venderid","vendername","sheetid","begindate","enddate","editdate","flag","status","seenum","contracttype")\
                                   .filter(**kwargs).order_by(orderStyle)

    paginator=Paginator(balanceList,20)
    try:
        balanceList=paginator.page(page)
    except Exception as e:
        print(e)

    # shopCodedistinct = []  #查询结果中，去重复的门店列表
    # for balance in balanceList:
    #     if balance.get('shopid') not in shopCodedistinct:
    #         shopCodedistinct.append(balance.get('shopid'))

    shopCodeStr = ''    #返回给pageFrom内部的shopcode表单
    for shop in shopId:
        shopCodeStr += shop+','

    return render(request,
                  'user_settle.html',
                  {"form":form,
                   "shopId":shopId,
                   "start":str(start),
                   "end":str(end),
                   "sheetId":sheetId,
                   "shopCodeStr":shopCodeStr,
                   # "shopCodedistinct":shopCodedistinct,
                   "status":status,
                   "orderStyle":orderStyle,
                   "balanceList":balanceList,
                   "page":page,
                   "grpName":grpName
                   })



def balanceArticle(request):
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    contracttype = request.session.get("s_contracttype")
    sheetId = request.GET.get('sheetid','')
    queryAction = request.POST.get('actionTxt','')
    #更新确认状态
    if queryAction == 'check':
        balanceObj = Billhead0.objects.get(sheetid__contains=sheetId,grpcode=grpCode)
        balanceObj.status='Y'
        balanceObj.save()

    #结算通知单汇总
    balanceList = Billhead0.objects.values("shopid","venderid","vendername","sheetid","paytype","begindate","enddate"
                                               ,"editdate","curdxvalue","payablemoney","kxinvoice","kxmoney","kxcash",
                                               "premoney","editor","checker","paychecker","contracttype")\
                                       .get(sheetid__contains=sheetId)

    if balanceList.get('kxinvoice'):
        cfpkx = float(round(balanceList.get('kxinvoice'),2))
    else:
        cfpkx = 0

    zkkx = float(round(balanceList.get('kxmoney')-balanceList.get('kxcash'),2))#帐扣扣项

    if balanceList.get('curdxvalue'):
        curdxValue = balanceList.get('curdxvalue')
    else:
        curdxValue = 0

    if balanceList.get('payablemoney'):
        payableMoney = float(balanceList.get('payablemoney'))
    else:
        payableMoney= 0

    if balanceList.get('premoney'):
        premoney = float(balanceList.get('premoney'))
    else:
        premoney = 0

    if curdxValue == 0:
        invoicePay = round((payableMoney-cfpkx),2)#应开票金额
        realPay = round((payableMoney-zkkx-premoney),2)#实付金额
    else:
        invoicePay = round((curdxValue-cfpkx),2)
        realPay = round((curdxValue-zkkx-premoney),2)


    #结算通知明细
    balanceItems = Billheaditem0.objects.values("inshopid","refsheettype","refsheetid","managedeptid","payabledate",
                                                "costvalue","costtaxvalue","costtaxrate")\
                                        .filter(sheetid__contains=sheetId)\
                                        .order_by("refsheettype","refsheetid","inshopid")

    totalCostValue = 0
    totalCostTax = 0
    i = 0
    for item in balanceItems:
        totalCostValue += item.get('costvalue',0)   #应结金额总额
        totalCostTax += item.get('costtaxvalue',0)  #税金总额
        i+=1
        item['lineIndex'] = i   #每条记录的行号
        item['managedeptid'] = str(item.get('managedeptid',0))

    payTypeDict = {"0":"其他","1":"支票","2":"电汇","3":"汇票"}

    return render(request,'user_settle_article.html',locals())