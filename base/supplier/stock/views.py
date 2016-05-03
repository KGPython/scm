# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect   #redirect 表单数据提交和页面重定向
import logging
from .forms import *
from base.models import BasShop,Stock
from django.db.models import Sum
import xlwt3
from django.db import connection

# Create your views here.
logger=logging.getLogger('base.supplier.stock.views')

def supplierStock(request):
    suppCode = request.session.get('s_suppcode')
    grpCode = request.session.get('s_grpcode')
    grpName = request.session.get('s_grpname').strip()

    stockList = []
    if request.method == 'POST':# 当提交表单时
        form = StockForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            shopCode = form.cleaned_data['shopCode']
            #proCode = form.cleaned_data['proCode']
            barcode = form.cleaned_data['barcode']
            num1 = form.cleaned_data['num1']
            num2 = form.cleaned_data['num2']
            if num1 >= 0:
                num1 = str(int(num1))
            if num2:
                num2 = str(int(num2))

            scCode = form.cleaned_data['scCode']
            proName = form.cleaned_data['proName']
            orderStyle = form.cleaned_data['orderStyle']

            kwargs = {}
            if len(shopCode):
                shopCode = shopCode[0:(len(shopCode)-1)]
                shopCode =shopCode.split(',')
                kwargs.setdefault("shopcode__in",shopCode)
            if barcode:
                kwargs.setdefault("barcode__contains",barcode.strip())
            if scCode:
                kwargs.setdefault("sccode__contains",scCode.strip())
            if proName:
                kwargs.setdefault("proname__contains",proName.strip())

            kwargs.setdefault("num__gte",num1)
            kwargs.setdefault("num__lte",num2)
            kwargs.setdefault("suppcode",suppCode)
            kwargs.setdefault("grpcode",grpCode)

            stockList = Stock.objects.values("shopcode")\
                                     .filter(**kwargs)\
                                     .annotate(num=Sum('num'),sums_intax=Sum('sums_intax'))\
                                     .order_by('-sums_intax')
            totalNum = 0  #总库存数量
            totalSumsIntax = 0  #总库存进价含税金额
            for stock in stockList:
                totalNum += stock.get('num',0)
                totalSumsIntax += stock.get('sums_intax',0)
            if request.GET.get('action', None)=="outExcel":
                title = '库存单据列表 '
                keyList = ['shopcode','num','sums_intax']#由excel展现字段决定
                rowTitle = [u'门店',u'库存数量',u'含税进价金额']
                rowTotal = [u'合计',totalNum,totalSumsIntax]
                return writeExcel(stockList,title,rowTitle,keyList,rowTotal)
        else:
            print(form.errors)
    else:
        form = StockForm()
        kwargs = {}
        num1 = "0"
        num2 = "100000"
        kwargs.setdefault("num__gte",num1)
        kwargs.setdefault("num__lte",num2)
        kwargs.setdefault("suppcode",suppCode)
        kwargs.setdefault("grpcode",grpCode)
        stockList = Stock.objects.values("shopcode")\
                                     .filter(**kwargs)\
                                     .annotate(num=Sum('num'),sums_intax=Sum('sums_intax'))\
                                     .order_by('-sums_intax')
        totalNum = 0  #总库存数量
        totalSumsIntax = 0  #总库存进价含税金额
        for stock in stockList:
            totalNum += stock.get('num',0)
            totalSumsIntax += stock.get('sums_intax',0)
    return render(request,'user_stock.html',locals())


def stockArticle(request):
    suppCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位

    shopCode = request.GET.get('shopcode', None)
    shopName = BasShop.objects.values("shopnm").get(shopcode=shopCode)
    shopName = shopName['shopnm'].strip()

    stockList = []
    if request.method == 'POST':# 当提交表单时
        form = StockForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            proCode = form.cleaned_data['proCode']
            barcode = form.cleaned_data['barcode']
            num1 = form.cleaned_data['num1']
            num2 = form.cleaned_data['num2']
            scCode = form.cleaned_data['scCode']
            proName = form.cleaned_data['proName']
            orderStyle = form.cleaned_data['orderStyle']

            kwargs = {}
            if barcode:
                kwargs.setdefault("barcode__contains",barcode.strip())
            if scCode:
                kwargs.setdefault("sccode__contains",scCode.strip())
            if proName:
                kwargs.setdefault("proname__contains",proName.strip())
            kwargs.setdefault("shopcode",shopCode)
            kwargs.setdefault("suppcode",suppCode)
            kwargs.setdefault("grpcode",grpCode)

            stockList = Stock.objects.values("shopcode","clearflag","sccode","scname","procode","proname","classes","unit","barcode","suppcode")\
                                     .filter(**kwargs)\
                                     .annotate(num=Sum('num'),sums_intax=Sum('sums_intax'))\
                                     .filter(num__gte=num1,num__lte=num2)\
                                     .order_by(orderStyle)
            totalNum = 0
            totalSumsIntax = 0
            for stock in stockList:
                totalNum += stock.get('num',0)
                totalSumsIntax += stock.get('sums_intax',0)
            if request.GET.get('action', None)!="outQuery":
                title = shopName+'库存明细表 '
                keyList = ['procode','proname','barcode','sccode','scname','classes','unit','num','sums_intax','clearflag']#由excel展现字段决定
                rowTitle = [u'商品编码',u'商品名称',u'商品条码',u'小类编码',u'小类名称',u'规格',u'单位',u'数量',u'含税进价金额',u'状态']
                rowTotal = ['',u'合计','','','','','',totalNum,totalSumsIntax,'']
                return writeExcel(stockList,title,rowTitle,keyList,rowTotal)

    else:
        form = StockForm(request.GET)
        kwargs = {}
        barcode =request.GET.get('barcode')
        num1 =request.GET.get('num1')
        num2 =request.GET.get('num2')
        scCode =request.GET.get('scCode')
        proName =request.GET.get('proName')
        orderStyle =request.GET.get('orderStyle')
        if not orderStyle:
            orderStyle='sums_intax'

        kwargs = {}
        if barcode:
            kwargs.setdefault("barcode__contains",barcode.strip())
        if scCode:
            kwargs.setdefault("sccode__contains",scCode.strip())
        if proName:
            kwargs.setdefault("proname__contains",proName.strip())
        kwargs.setdefault("shopcode",shopCode)
        kwargs.setdefault("suppcode",suppCode)
        kwargs.setdefault("grpcode",grpCode)

        stockList = Stock.objects.values("shopcode","clearflag","sccode","scname","procode","proname",'classes',"unit","barcode","suppcode")\
                                     .filter(**kwargs)\
                                     .annotate(num=Sum('num'),sums_intax=Sum('sums_intax'))\
                                     .filter(num__gte=num1,num__lte=num2).order_by(orderStyle)
        totalNum = 0
        totalSumsIntax = 0
        for stock in stockList:
            totalNum += stock.get('num',0)
            totalSumsIntax += stock.get('sums_intax',0)

    goodsFlag = {"0":"正常","1":"暂停订货","2":"暂停销售","3":"已清退","5":"暂停经营","6":"待清退","7":"待启用","8":"新品"}
    return render(request,'user_stock_article.html',locals())


def stockDetail(request):
    suppCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname').strip()

    if request.method == 'POST':# 当提交表单时
        form = StockForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            shopCode = form.cleaned_data['shopCode']
            barcode = form.cleaned_data['barcode']
            num1 = str(form.cleaned_data['num1'])
            num2 = str(form.cleaned_data['num2'])
            scCode = form.cleaned_data['scCode']
            proName = form.cleaned_data['proName']
            orderStyle = form.cleaned_data['orderStyle']

            if shopCode:
                shopStr=shopCode[0:len(shopCode)-1]
                shopCodeList = shopStr.split(",")
                shopCode ="'"
                for item in shopCodeList:
                    shopCode +=str(item)
                    shopCode +="','"
                shopCode = shopCode[0:len(shopCode)-2]

                #shopcode,
                sql ="select * from (select '',(select name from BRAND,bas_product  where pcode=tb1.procode and id=prodmark) brandnm,sccode,scname,procode,proname,classes,unit,fprocode,sum(num) num,sum(sums_intax) sums_intax,barcode from(select shopcode,sccode,scname,procode,proname,classes,unit,num,sums_intax,barcode,fprocode from stock where shopcode in ("+shopCode+") and barcode like '%"+barcode.strip()+"%' and sccode like '%"+scCode.strip()+"%' and proname like '%"+proName.strip()+"%' and suppcode='"+suppCode+"' and grpcode='"+grpCode+"') as tb1 group by brandnm,sccode,scname,procode,proname,fprocode,classes,unit,barcode) as tb2 where num>="+num1+" and num<="+num2+" order by "+orderStyle
            else:
                sql ="select * from (select '',(select name from BRAND,bas_product  where pcode=tb1.procode and id=prodmark) brandnm,sccode,scname,procode,proname,classes,unit,fprocode,sum(num) num,sum(sums_intax) sums_intax,barcode from(select shopcode,sccode,scname,procode,proname,classes,unit,num,sums_intax,barcode,fprocode from stock where barcode like '%"+barcode.strip()+"%' and sccode like '%"+scCode.strip()+"%' and proname like '%"+proName.strip()+"%' and suppcode='"+suppCode+"' and grpcode='"+grpCode+"') as tb1 group by brandnm,sccode,scname,procode,proname,fprocode,classes,unit,barcode) as tb2 where num>="+num1+" and num<="+num2+" order by "+orderStyle

            cursor = connection.cursor()
            cursor.execute(sql)
            fetchall = cursor.fetchall()
            cursor.close()
            connection.close()

            stockList = []
            total_sums_intax = 0
            total_sums = 0
            for obj in fetchall:
                dic={}
                dic['sccode']=obj[2]
                dic['scname']=obj[3]
                dic['procode']=obj[4]
                dic['proname']=obj[5]
                dic['classes']=obj[6]
                dic['unit']=obj[7]
                dic['num']=obj[9]
                dic['sums_intax']=obj[10]
                dic['barcode']=obj[11]
                total_sums_intax +=obj[10]
                total_sums += obj[9]
                stockList.append(dic)
            if request.GET.get('action', None)!="outQuery":
                title = '全部库存明细列表 '
                keyList = ['procode','proname','barcode','sccode','scname','classes','unit','num','sums_intax']#由excel展现字段决定
                rowTitle = [u'商品编码',u'商品名称',u'商品条码',u'小类编码',u'小类名称',u'规格',u'单位',u'数量',u'含税进价金额']
                rowTotal = ['',u'合计','','','','','',total_sums,total_sums_intax]
                return writeExcel(stockList,title,rowTitle,keyList,rowTotal)

    else:
        form = StockForm()
        num1 = "0"
        num2 = "100000"
        sql ="select * from (select '',(select name from BRAND,bas_product  where pcode=tb1.procode and id=prodmark) brandnm,sccode,scname,procode,proname,classes,unit,fprocode,sum(num) num,sum(sums_intax) sums_intax,barcode from(select shopcode,sccode,scname,procode,proname,classes,unit,num,sums_intax,barcode,fprocode from stock where suppcode='"+suppCode+"' and grpcode='"+grpCode+"') as tb1 group by brandnm,sccode,scname,procode,proname,fprocode,classes,unit,barcode) as tb2 where num>="+num1+" and num<="+num2+" order by sccode"
        cursor = connection.cursor()
        cursor.execute(sql)
        fetchall = cursor.fetchall()
        cursor.close()
        connection.close()

        stockList = []
        total_sums_intax = 0
        total_sums = 0
        for obj in fetchall:
            dic={}
            dic['sccode']=obj[2]
            dic['scname']=obj[3]
            dic['procode']=obj[4]
            dic['proname']=obj[5]
            dic['classes']=obj[6]
            dic['unit']=obj[7]
            dic['num']=obj[9]
            dic['sums_intax']=obj[10]
            dic['barcode']=obj[11]
            total_sums_intax +=obj[10]
            total_sums += obj[9]
            stockList.append(dic)

    return render(request,'user_stockDetail.html',locals())


def detailArticle(request):
    suppCode = request.session.get('s_suppcode')   #用户所属单位
    grpCode = request.session.get('s_grpcode')   #用户所属单位
    grpName = request.session.get('s_grpname')

    #获取列表页传递的参数
    shopCode = request.REQUEST.get('shopcode','')
    proCode = request.REQUEST.get('procode','')
    num1 = str( request.REQUEST.get('num1',''))
    num2 = str( request.REQUEST.get('num2',''))
    proName = request.REQUEST.get('proname','').strip()

    if shopCode:
        shopCode=shopCode[0:len(shopCode)]
        sql ="select t1.shopcode,shopnm,num,sums_intax,clearflag from(select shopcode,sum(num) num,sum(sums_intax) sums_intax,clearflag from stock where shopcode in ("+shopCode+") and procode like '%"+proCode+"%' and suppcode='"+suppCode+"' and grpcode='"+grpCode+"' group by shopcode,clearflag) as t1,bas_shop as t2 where t2.grpcode=grpcode and t1.num>="+num1+" and t1.num<="+num2+" and t1.shopcode=t2.shopcode"
    else:
        sql ="select t1.shopcode,shopnm,num,sums_intax,clearflag from(select shopcode,sum(num) num,sum(sums_intax) sums_intax,clearflag from stock where procode like '%"+proCode+"%' and suppcode='"+suppCode+"' and grpcode='"+grpCode+"' group by shopcode,clearflag) as t1,bas_shop as t2 where t2.grpcode=grpcode and t1.num>="+num1+" and t1.num<="+num2+" and t1.shopcode=t2.shopcode"

    cursor = connection.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    cursor.close()
    connection.close()
    stockList = []
    total_num = 0
    total_sums_intax = 0
    for obj in fetchall:
        dic={}
        dic['shopcode']=obj[0]
        dic['shopnm']=obj[1]
        dic['num']=obj[2]
        dic['sums_intax']=obj[3]
        dic['clearflag']=obj[4]
        total_num +=obj[2]
        total_sums_intax += obj[3]
        stockList.append(dic)

    flagDict= {"0":u"正常","1":u"暂停订货","2":u"暂停销售","3":u"已清退","5":u"暂停经营","6":u"待清退","7":u"待启用","8":u"新品"}

    if request.GET.get('action', None)=="outExcel":
        title = '单品:'+proName+'库存单明细 '
        keyList = ['shopnm','num','sums_intax','clearflag']#由excel展现字段决定
        rowTitle = [u'门店',u'数量',u'含税进价',u'商品该门店状态']
        rowTotal = [u'合计',total_num,total_sums_intax,'']
        return writeExcel(stockList,title,rowTitle,keyList,rowTotal)
    return render(request,'user_stockDetail_article.html',locals())

def set_style(name,height,bold=False):
    style = xlwt3.XFStyle()

    font = xlwt3.Font()
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height

    align = xlwt3.Alignment()
    align.horz = xlwt3.Alignment.HORZ_CENTER
    align.vert = xlwt3.Alignment.VERT_CENTER

    borders= xlwt3.Borders()
    borders.left= xlwt3.Borders.DASHED
    borders.right = xlwt3.Borders.DASHED
    borders.top = xlwt3.Borders.DASHED
    borders.bottom = xlwt3.Borders.DASHED
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40

    style.alignment = align
    style.font = font
    style.borders = borders

    return style

def writeExcel(list,title,rowTitle,keyList,rowTotal):
    f = xlwt3.Workbook()

    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)
    #标题
    sheet1.write_merge(0,0,0,len(rowTitle)-1,title,set_style('Times New Roman',290,True))
    #第一行表头
    for i in range(0,len(rowTitle)):
        sheet1.write(1,i,rowTitle[i],set_style('Arial',230,True))
    #数据主体
    stylebody = set_style('Arial',230)
    for i in range(0,len(list)):
        for j in range(0,len(keyList)):
            sheet1.write(i+2,j,list[i].get(keyList[j]),stylebody)
            sheet1.col(j).width = 7000      #单元格宽度
    #最后一行合计
    for i in range(0,len(rowTotal)):
        sheet1.write(len(list)+2,i,rowTotal[i],set_style('Arial',220,True))

    response = HttpResponse()
    response['Content-Type']='application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename=example.xls'
    response['Pragma'] = "no-cache"
    response['Expires'] = "0"
    f.save(response)
    return response






