from django.shortcuts import render
from django.http import HttpResponse
import datetime,decimal
import xlwt3 as xlwt
from base.models import Kglossrate,BasPurLog
from base.utils import MethodUtil as mth
from base.utils import DateUtil
import json
from django.views.decorators.cache import cache_page

def query(timeStart,timeEnd):
    karrs = {}
    karrs.setdefault('checkdate__lte', timeEnd)
    karrs.setdefault('checkdate__gte', timeStart)
    data = Kglossrate.objects.\
                values('shopid', 'shopname', 'sheetid', 'goodsid', 'goodsname', 'deptid', 'deptname',
                                     'askqty', 'checkqty', 'qty', 'costvalue') \
                .filter(**karrs).exclude(shopid='C009').order_by('shopid')
    for item in data:
        for key in item.keys():
            if isinstance(item[key], decimal.Decimal):
                item[key] = float('%0.2f' % item[key])

    return locals()

@cache_page(60 * 2 ,key_prefix='loss_rate_100')
def index(request):
    ucode = request.session.get("s_ucode")
    uname = request.session.get("s_uname")
    timeStart = datetime.date.today()-datetime.timedelta(days=1)
    timeEnd = datetime.date.today()

    # 操作日志
    qtype = mth.getReqVal(request, "qtype", "1")
    if not qtype:
        qtype = "1"
    key_state = mth.getReqVal(request, "key_state", '')
    if qtype == '2' and (not key_state or key_state != '2'):
        qtype = '1'
    path = request.path
    today = datetime.datetime.today()
    BasPurLog.objects.create(name="单品报损超100", url=path, qtype=qtype, ucode=ucode, uname=uname, createtime=today)

    if qtype== "1":
        data = query(timeStart,timeEnd)
        return render(request, 'report/abnormal/loss_rate.html', data)
    else:
        yesterday = DateUtil.get_day_of_day(-1)
        name = '_loss_rate100'
        fname = yesterday.strftime('%m.%d')+name+".xls"
        return export(fname,timeStart,timeEnd)


import base.report.Excel as excel
def export(fname,timeStart,timeEnd):
    if not excel.isExist(fname):
        res = query(timeStart,timeEnd)
        data = res['data']
        createExcel(fname, data)
    res = {}
    res['fname'] = fname
    return HttpResponse(json.dumps(res))

def createExcel(fname,data):
    wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
    writeDataToSheet2(wb, data)
    excel.saveToExcel(fname, wb)

def writeDataToSheet2(wb,data):
    date = DateUtil.get_day_of_day(-1)
    year = date.year
    month = date.month

    sheet2 = wb.add_sheet("单品报损超100",cell_overwrite_ok=True)
    titlesSheet2 = [
        [("单品报损超100",0,1,12)],
        [("报表日期",8,1,1),("%s年-%s月-%s日"%(year,month,date.day),9,1,3)],
        [
            ("机构编号",0,1,1),("机构名称",1,1,1),("单据编号",2,1,1),("商品名称",3,1,1),("商品编码",4,1,1),
            ("类别编码",5,1,1),("类别名称",6,1,1),("申请数量",7,1,1),("审批数量",8,1,1),("实际报损数",9,1,1),
            ("成本金额",10,1,1),("解释原因",11,1,1)
        ]
    ]
    keylistSheet2 = ['shopid','shopname','sheetid','goodsid','goodsname','deptid','deptname',
                     'askqty','checkqty','qty','costvalue''reason']
    widthList = [600,600,600,600,1000,600,600,600,600,600,600,1000]

    mth.insertTitle2(sheet2,titlesSheet2,keylistSheet2,widthList)
    mth.insertCell2(sheet2,3,data,keylistSheet2,None)