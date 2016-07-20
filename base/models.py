#-*- coding:utf-8  -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

import json,datetime,decimal
from django.db import models

class EstimateYear(models.Model):
    shopid = models.CharField(db_column='ShopID', max_length=12, blank=True, null=True)  # Field name made lowercase.
    dateid = models.DateField(db_column='DateID', blank=True, null=True)  # Field name made lowercase.
    salevalue = models.DecimalField(db_column='SaleValue', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salegain = models.DecimalField(db_column='SaleGain', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estimate_year'

class BasPurLog(models.Model):
    name = models.CharField(db_column='Name', max_length=32, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=100, blank=True, null=True)  # Field name made lowercase.
    qtype = models.SmallIntegerField(db_column='Qtype', blank=True, null=True)  # Field name made lowercase.
    ucode = models.CharField(db_column='Ucode', max_length=16, blank=True, null=True)  # Field name made lowercase.
    uname = models.CharField(db_column='Uname', max_length=32, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_pur_log'

class Kgprofit(models.Model):
    bbdate = models.DateTimeField(auto_now_add=True)
    sdate = models.DateTimeField(auto_now_add=True)
    shopid = models.CharField(max_length=4)
    shopname = models.CharField(max_length=64)
    goodsid = models.IntegerField()
    goodsname = models.CharField(max_length=64)
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    deptname = models.CharField(max_length=64)
    qty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    salevalue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discvalue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    truevalue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    costvalue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stockqty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KGprofit'


class BasShopGroup(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40)  # Field name made lowercase.
    parent = models.IntegerField(db_column='Parent', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_shop_group'

class Billhead0Status(models.Model):
    sheetid = models.CharField(db_column='SheetId', max_length=32, blank=True, null=True)  # Field name made lowercase.
    inviocestatus = models.SmallIntegerField(db_column='InvioceStatus', blank=True, null=True)  # Field name made lowercase.
    flag = models.SmallIntegerField(db_column='Flag', blank=True, null=True)  # Field name made lowercase.
    shopid = models.CharField(db_column='Shopid', max_length=4, blank=True, null=True)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='Editdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    venderid = models.BigIntegerField(db_column='Venderid', blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'billhead0_status'

class Estimate(models.Model):
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    datetype = models.IntegerField(db_column='DateType')  # Field name made lowercase.
    dateid = models.DateTimeField(db_column='DateID',auto_now_add=True)  # Field name made lowercase.
    deptlevelid = models.IntegerField(db_column='DeptLevelID')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    weatherid = models.IntegerField(db_column='WeatherID')  # Field name made lowercase.
    salevalue = models.DecimalField(db_column='SaleValue', max_digits=12, decimal_places=2)  # Field name made lowercase.
    salegain = models.DecimalField(db_column='SaleGain', max_digits=12, decimal_places=2)  # Field name made lowercase.
    stockvalue = models.DecimalField(db_column='StockValue', max_digits=12, decimal_places=2)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Estimate'
        unique_together = (('dateid', 'groupid', 'shopid'),)

class BasShopRegion(models.Model):
    shopid = models.CharField(db_column='ShopId', max_length=8, blank=True, null=True)  # Field name made lowercase.
    shopname = models.CharField(db_column='ShopName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=8, blank=True, null=True)  # Field name made lowercase.
    opentime = models.DateTimeField(db_column='OpenTime', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=8, blank=True, null=True)  # Field name made lowercase.
    shoptype = models.IntegerField(db_column='ShopType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_shop_region'

class Kshopsale(models.Model):
    sdate = models.DateTimeField(db_column='Sdate',auto_now_add=True)  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    salevalue = models.DecimalField(db_column='Salevalue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salegain = models.DecimalField(db_column='Salegain', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tradenumber = models.DecimalField(db_column='Tradenumber', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tradeprice = models.DecimalField(db_column='Tradeprice', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salevalueesti = models.DecimalField(db_column='SalevalueEsti', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salegainesti = models.DecimalField(db_column='SalegainEsti', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    sdateold = models.DateTimeField(db_column='Sdateold', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    tradenumberold = models.DecimalField(db_column='Tradenumberold', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tradepriceold = models.DecimalField(db_column='Tradepriceold', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salevalueold = models.DecimalField(db_column='Salevalueold', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    salegainold = models.DecimalField(db_column='Salegainold', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Kshopsale'
        unique_together = (('sdate', 'shopid'),)


class Ret0(models.Model):
    sheetid = models.CharField(db_column='SheetID', primary_key=True, max_length=16)  # Field name made lowercase.
    refsheetid = models.CharField(db_column='refSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    shopid = models.CharField(max_length=4)
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    retdate = models.DateTimeField(auto_now_add=True)
    paymoney = models.DecimalField(db_column='PayMoney', max_digits=12, decimal_places=2)  # Field name made lowercase.
    kxsummoney = models.DecimalField(db_column='KxSumMoney', max_digits=12, decimal_places=2)  # Field name made lowercase.
    acceptflag = models.IntegerField(db_column='AcceptFlag')  # Field name made lowercase.
    badflag = models.IntegerField(db_column='BadFlag')  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=64, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    editor = models.CharField(db_column='Editor', max_length=8)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    finchecker = models.CharField(db_column='FinChecker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    managedeptid = models.IntegerField()
    placeid = models.IntegerField(db_column='PlaceID', blank=True, null=True)  # Field name made lowercase.
    mastervenderid = models.IntegerField(db_column='MasterVenderID')  # Field name made lowercase.
    printcount = models.IntegerField(db_column='PrintCount')  # Field name made lowercase.
    emailflag = models.IntegerField()
    cprintcount = models.IntegerField(db_column='cPrintCount')  # Field name made lowercase.
    costflag = models.IntegerField()
    overrule = models.CharField(max_length=100, blank=True, null=True)
    kxcalculated = models.IntegerField(db_column='KXCalculated')  # Field name made lowercase.
    isadjust = models.IntegerField(db_column='IsAdjust')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ret0'


class Retitem0(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    cost = models.DecimalField(max_digits=12, decimal_places=4)
    askqty = models.DecimalField(max_digits=12, decimal_places=3)
    planqty = models.DecimalField(max_digits=12, decimal_places=3)
    realqty = models.DecimalField(max_digits=12, decimal_places=3)
    reasontypeid = models.IntegerField(db_column='ReasonTypeID')  # Field name made lowercase.
    reason = models.CharField(max_length=200, blank=True, null=True)
    logistics = models.IntegerField()
    pknum = models.IntegerField(db_column='PkNum')  # Field name made lowercase.
    pkname = models.CharField(db_column='PKName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    pkspec = models.CharField(db_column='PKSpec', max_length=12, blank=True, null=True)  # Field name made lowercase.
    subitem_iid = models.IntegerField()
    stockqty = models.DecimalField(db_column='stockQty', max_digits=12, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    goodscostid = models.IntegerField(db_column='GoodsCostid')  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=300, blank=True, null=True)  # Field name made lowercase.
    inputgoodsid = models.CharField(db_column='InputGoodsId', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'retitem0'
        unique_together = (('sheetid','goodsid', 'goodscostid'),)

class Adprice(models.Model):
    code = models.CharField(db_column='Code', max_length=20)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=4)  # Field name made lowercase.
    shopname = models.CharField(db_column='Shopname', max_length=40)  # Field name made lowercase.
    spercode = models.CharField(db_column='Spercode', max_length=20)  # Field name made lowercase.
    chdate = models.DateField(db_column='Chdate',auto_now_add=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cstyle = models.CharField(db_column='Cstyle', max_length=20)  # Field name made lowercase.
    csname = models.CharField(db_column='Csname', max_length=20)  # Field name made lowercase.
    concode = models.CharField(db_column='Concode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=20)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    seenum = models.IntegerField(db_column='Seenum', blank=True, null=True)  # Field name made lowercase.
    spername = models.CharField(db_column='Spername', max_length=64, blank=True, null=True)  # Field name made lowercase.
    adpriceclass = models.CharField(db_column='Adpriceclass', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateField(db_column='Bdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    edate = models.DateField(db_column='Edate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adprice'
        unique_together = (('code', 'shopcode', 'spercode', 'chdate', 'cstyle', 'sstyle', 'grpcode'),)


class Adpriced(models.Model):
    code = models.CharField(db_column='Code', max_length=20)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    procde = models.CharField(db_column='Procde', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cprice_notax = models.DecimalField(db_column='Cprice_Notax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sprice = models.DecimalField(db_column='Sprice', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum = models.DecimalField(db_column='Anum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_notax = models.DecimalField(db_column='Anum_Notax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_intax = models.DecimalField(db_column='Anum_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_stock = models.DecimalField(db_column='Anum_Stock', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_stock_intax = models.DecimalField(db_column='Anum_Stock_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_stock_notax = models.DecimalField(db_column='Anum_Stock_Notax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_sale = models.DecimalField(db_column='Anum_Sale', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_sale_intax = models.DecimalField(db_column='Anum_Sale_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_sale_notax = models.DecimalField(db_column='Anum_Sale_Notax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_other = models.DecimalField(db_column='Anum_Other', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_other_iitax = models.DecimalField(db_column='Anum_Other_Iitax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    anum_other_notax = models.DecimalField(db_column='Anum_Other_Notax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    chdate = models.DateField(db_column='Chdate',auto_now_add=True)  # Field name made lowercase.
    pcode = models.CharField(db_column='Pcode', max_length=15)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=20)  # Field name made lowercase.
    pname = models.CharField(db_column='Pname', max_length=64, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='Spec', max_length=20, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=8, blank=True, null=True)  # Field name made lowercase.
    newtax = models.DecimalField(db_column='Newtax', max_digits=8, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    dqhsjj = models.IntegerField(db_column='Dqhsjj', blank=True, null=True)  # Field name made lowercase.
    adbatchseq = models.DecimalField(db_column='Adbatchseq', max_digits=10, decimal_places=0)  # Field name made lowercase.
    mll = models.DecimalField(db_column='Mll', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    tzje = models.DecimalField(db_column='Tzje', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    spercode = models.CharField(db_column='Spercode', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'adpriced'
        unique_together = (('code', 'pcode', 'adbatchseq','spercode'),)

class BasBarcode(models.Model):
    barcodeid = models.CharField(db_column='BarcodeID', max_length=20)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    pkname = models.CharField(db_column='PKName', max_length=8)  # Field name made lowercase.
    pknum = models.IntegerField(db_column='PKNum')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    pkspec = models.CharField(db_column='PKspec', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_barcode'


class BasCounter(models.Model):
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    ctcode = models.CharField(db_column='Ctcode', max_length=20)  # Field name made lowercase.
    suppcode = models.CharField(db_column='Suppcode', max_length=20)  # Field name made lowercase.
    nm = models.CharField(db_column='Nm', max_length=40, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='Enddate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    begindate = models.DateTimeField(db_column='Begindate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_counter'
        unique_together = (('grpcode', 'shopcode', 'ctcode', 'suppcode'),)


class BasFee(models.Model):
    bid = models.IntegerField(db_column='BID',primary_key=True)  # Field name made lowercase.
    suppcode = models.CharField(db_column='SUPPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ucode = models.CharField(db_column='UCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bsum = models.DecimalField(db_column='BSUM', max_digits=16, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bdate = models.DateField(db_column='BDATE', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    begindate = models.DateField(db_column='BEGINDATE', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='ENDDATE', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bfdate = models.DateField(db_column='BFDATE', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    suppcodeid = models.CharField(db_column='SUPPCODEID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    def toDict(self):
        lst = []
        try:
            for attr in [f.name for f in self._meta.fields]:
                value = getattr(self, attr)
                if isinstance(value,datetime.date):
                    value = value.strftime('%Y-%m-%d')
                elif isinstance(value,decimal.Decimal):
                    value = "%0.2f" % value
                tup = (attr,value)
                lst.append(tup)
        except Exception as e:
            print(e)
        return dict(lst)

    class Meta:
        managed = False
        db_table = 'bas_fee'


class BasFeesum(models.Model):
    bid = models.IntegerField(db_column='BID')  # Field name made lowercase.
    suppcode = models.CharField(db_column='SUPPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ucode = models.CharField(db_column='UCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supsum = models.DecimalField(db_column='SUPSUM', max_digits=16, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bfdate = models.DateField(db_column='BFDATE',auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_feesum'


class BasGoods(models.Model):
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64)  # Field name made lowercase.
    unitname = models.CharField(db_column='UnitName', max_length=20)  # Field name made lowercase.
    spec = models.CharField(db_column='Spec', max_length=50, blank=True, null=True)  # Field name made lowercase.
    brandid = models.IntegerField(db_column='BrandID')  # Field name made lowercase.
    deptid = models.CharField(db_column='DeptID', max_length=50)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    costtaxrate = models.DecimalField(db_column='CostTaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    dkrate = models.DecimalField(db_column='DKRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    promflag = models.IntegerField(db_column='PromFlag')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    barcodeid = models.CharField(db_column='BarcodeID', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_goods'


class BasGroup(models.Model):
    grpcode = models.CharField(db_column='GRPCODE', max_length=20,primary_key=True)  # Field name made lowercase.
    grpnm = models.CharField(db_column='GRPNM', max_length=40, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='MANAGER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=20, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='PROVINCE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='CITY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_group'


class BasKe(models.Model):
    kbcode = models.CharField(db_column='KBCODE', max_length=10)  # Field name made lowercase.
    kbname = models.CharField(db_column='KBNAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_ke'


class BasOrg(models.Model):
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    orgcode = models.CharField(db_column='Orgcode', max_length=20)  # Field name made lowercase.
    tier = models.CharField(db_column='Tier', max_length=20)  # Field name made lowercase.
    orgname = models.CharField(db_column='Orgname', max_length=20)  # Field name made lowercase.
    parentcode = models.CharField(db_column='Parentcode', max_length=20)  # Field name made lowercase.
    orgtype = models.CharField(db_column='Orgtype', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_org'
        unique_together = (('grpcode', 'orgcode'),)


class BasPchild(models.Model):
    pccode = models.CharField(db_column='PCCODE', max_length=20)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='SPEC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_pchild'


class BasProdClass(models.Model):
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    classx = models.CharField(db_column='Classx', max_length=50)  # Field name made lowercase.
    nm = models.CharField(db_column='Nm', max_length=50)  # Field name made lowercase.
    ctype = models.CharField(db_column='Ctype', max_length=20)  # Field name made lowercase.
    parentcode = models.CharField(db_column='Parentcode', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_prod_class'
        unique_together = (('grpcode', 'classx'),)


class BasProduct(models.Model):
    pcode = models.CharField(db_column='Pcode', primary_key=True, max_length=20)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    chnm = models.CharField(db_column='Chnm', max_length=64)  # Field name made lowercase.
    ennm = models.CharField(db_column='Ennm', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sizex = models.CharField(db_column='Sizex', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prodmark = models.CharField(db_column='Prodmark', max_length=20, blank=True, null=True)  # Field name made lowercase.
    produceplace = models.CharField(db_column='Produceplace', max_length=32, blank=True, null=True)  # Field name made lowercase.
    packstyle = models.CharField(db_column='Packstyle', max_length=20, blank=True, null=True)  # Field name made lowercase.
    property = models.CharField(db_column='Property', max_length=50, blank=True, null=True)  # Field name made lowercase.
    pricebatch = models.DecimalField(db_column='Pricebatch', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    pricesale = models.DecimalField(db_column='Pricesale', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    image_path = models.CharField(db_column='Image_Path', max_length=20, blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=64, blank=True, null=True)  # Field name made lowercase.
    classx = models.CharField(db_column='Classx', max_length=50, blank=True, null=True)  # Field name made lowercase.
    classxnm = models.CharField(db_column='Classxnm', max_length=50, blank=True, null=True)  # Field name made lowercase.
    suppcode = models.CharField(db_column='Suppcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cshh = models.CharField(db_column='Cshh', max_length=20, blank=True, null=True)  # Field name made lowercase.
    spstatus = models.CharField(db_column='Spstatus', max_length=2, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_product'


class BasPur(models.Model):
    pcode = models.CharField(db_column='PCODE', max_length=20)  # Field name made lowercase.
    nm = models.CharField(db_column='NM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    bmoudule = models.CharField(db_column='BMOUDULE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    cmoudule = models.CharField(db_column='CMOUDULE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    special = models.CharField(db_column='SPECIAL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parent_nm = models.CharField(db_column='PARENT_NM', max_length=60, blank=True, null=True)  # Field name made lowercase.
    grpname = models.CharField(db_column='GRPNAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    border = models.CharField(db_column='BORDER', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_pur'


class BasPurChild(models.Model):
    pcode = models.CharField(db_column='PCODE', max_length=20)  # Field name made lowercase.
    pccode = models.CharField(db_column='PCCODE', max_length=20)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='SPEC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_pur_child'


class BasRole(models.Model):
    rcode = models.CharField(db_column='RCODE',primary_key=True, max_length=20)  # Field name made lowercase.
    nm = models.CharField(db_column='NM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=10, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_role'


class BasSuppLand(models.Model):
    grpcode = models.CharField(db_column='GRPCODE', max_length=20)  # Field name made lowercase.
    suppcode = models.CharField(db_column='SUPPCODE', max_length=20)  # Field name made lowercase.
    landcs = models.IntegerField(db_column='LANDCS', blank=True, null=True)  # Field name made lowercase.
    lastlandtime = models.DateTimeField(db_column='LASTLANDTIME', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ylzd1 = models.CharField(db_column='YLZD1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ylzd2 = models.CharField(db_column='YLZD2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    allcs = models.IntegerField(db_column='ALLCS', blank=True, null=True)  # Field name made lowercase.
    utype = models.CharField(db_column='UTYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    supname = models.CharField(db_column='SUPNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_supp_land'
		
class BasRolePur(models.Model):
    rcode = models.CharField(db_column='RCODE', max_length=20)  # Field name made lowercase.
    pcode = models.CharField(db_column='PCODE', max_length=20)  # Field name made lowercase.
    pccode = models.CharField(db_column='PCCODE', max_length=20)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_role_pur'



class BasShop(models.Model):
    grpcode = models.CharField(db_column='Grpcode',primary_key=True, max_length=10)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    shopnm = models.CharField(db_column='Shopnm', max_length=40)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=80, blank=True, null=True)  # Field name made lowercase.
    manager = models.CharField(db_column='Manager', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=32, blank=True, null=True)  # Field name made lowercase.
    shoptype = models.CharField(db_column='Shoptype', max_length=20, blank=True, null=True)  # Field name made lowercase.
    deptcode = models.CharField(db_column='Deptcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shopname = models.CharField(db_column='Shopname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cdno = models.CharField(db_column='Cdno', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_shop'
        unique_together = (('grpcode', 'shopcode'),)

class Stock(models.Model):
    goodscostid = models.CharField(db_column='GoodsCostID', max_length=255,primary_key=True)  # Field name made lowercase.
    procode = models.CharField(db_column='Procode', max_length=20)  # Field name made lowercase.
    proname = models.CharField(db_column='Proname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    proclass = models.CharField(db_column='Proclass', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fprocode = models.CharField(db_column='Fprocode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    sccode = models.CharField(db_column='Sccode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    scname = models.CharField(db_column='Scname', max_length=60, blank=True, null=True)  # Field name made lowercase.
    classes = models.CharField(db_column='Classes', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num = models.DecimalField(db_column='Num', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    avprice_intax = models.DecimalField(db_column='Avprice_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sums_intax = models.DecimalField(db_column='Sums_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sums = models.DecimalField(db_column='Sums', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sttime = models.DateTimeField(db_column='Sttime', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='Endtime', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    departcode = models.CharField(db_column='Departcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sdepartno = models.CharField(db_column='Sdepartno', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=20, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    suppcode = models.CharField(db_column='Suppcode', max_length=6)  # Field name made lowercase.
    fsdate = models.DateTimeField(db_column='Fsdate',auto_now_add=True)  # Field name made lowercase.
    clearflag = models.IntegerField(db_column="clearflag",blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'
        unique_together = (('goodscostid', 'procode', 'grpcode', 'shopcode', 'suppcode'),)

class BasStub(models.Model):
    itemid = models.CharField(db_column='ITEMID', max_length=20,primary_key=True)  # Field name made lowercase.
    itemnm = models.CharField(db_column='ITEMNM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prefix = models.CharField(db_column='PREFIX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lastnum = models.CharField(db_column='LASTNUM', max_length=20, blank=True, null=True)  # Field name made lowercase.
    numlen = models.IntegerField(db_column='NUMLEN', blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_stub'




class BasSupplier(models.Model):
    suppcode = models.CharField(db_column='Suppcode', max_length=8,primary_key=True)  # Field name made lowercase.
    chnm = models.CharField(db_column='Chnm', max_length=64)  # Field name made lowercase.
    ennm = models.CharField(db_column='Ennm', max_length=50, blank=True, null=True)  # Field name made lowercase.
    linkmen = models.CharField(db_column='Linkmen', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taxno = models.CharField(db_column='Taxno', max_length=40, blank=True, null=True)  # Field name made lowercase.
    accountno = models.CharField(db_column='Accountno', max_length=40, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=64, blank=True, null=True)  # Field name made lowercase.
    bank = models.CharField(db_column='Bank', max_length=128, blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lastdate = models.DateTimeField(db_column='Lastdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    postcode = models.CharField(db_column='Postcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=20, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=100, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mastervenderid = models.CharField(db_column='Mastervenderid', max_length=8, blank=True, null=True)  # Field name made lowercase.
    concode = models.CharField(db_column='Concode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contracttype = models.CharField(db_column='contracttype', max_length=2, blank=True, null=True)  # Field name made lowercase.
    paytypeid = models.CharField(db_column='PayTypeid', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_supplier'
        unique_together = (('suppcode', 'grpcode'),)


class BasUser(models.Model):
    ucode = models.CharField(db_column='UCODE', max_length=20,primary_key=True)  # Field name made lowercase.
    nm = models.CharField(db_column='NM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dept = models.CharField(db_column='DEPT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    depttype = models.CharField(db_column='DEPTTYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    utype = models.CharField(db_column='UTYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20)  # Field name made lowercase.
    rangee = models.CharField(db_column='RANGEE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    budate = models.DateField(db_column='BUDATE', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    def toDict(self):
        lst = []
        try:
            for attr in [f.name for f in self._meta.fields]:
                value = getattr(self, attr)
                if isinstance(value,datetime.date):
                    value = value.strftime('%Y-%m-%d')
                tup = (attr,value)
                lst.append(tup)
        except Exception as e:
            print(e)
        return dict(lst)

    class Meta:
        managed = False
        db_table = 'bas_user'


class BasUserClass(models.Model):
    tablecode = models.CharField(db_column='TABLECODE', max_length=20)  # Field name made lowercase.
    ucode = models.CharField(db_column='UCODE', max_length=10)  # Field name made lowercase.
    orgcode = models.CharField(db_column='ORGCODE', max_length=30)  # Field name made lowercase.
    colcode = models.CharField(db_column='COLCODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=2)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_user_class'
        unique_together = (('tablecode', 'ucode', 'orgcode'),)


class BasUserRole(models.Model):
    ucode = models.CharField(db_column='UCODE', max_length=20)  # Field name made lowercase.
    rcode = models.CharField(db_column='RCODE', max_length=20)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GRPCODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    brdate = models.DateField(db_column='BRDATE', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bas_user_role'


class BillIn(models.Model):
    code = models.CharField(db_column='Code', max_length=20)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    chdate = models.DateTimeField(db_column='Chdate',auto_now_add=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=64, blank=True, null=True)  # Field name made lowercase.
    spercode = models.CharField(db_column='Spercode', max_length=20)  # Field name made lowercase.
    spername = models.CharField(db_column='Spername', max_length=64, blank=True, null=True)  # Field name made lowercase.
    edate = models.DateTimeField(db_column='Edate',auto_now_add=True)  # Field name made lowercase.
    ordercode = models.CharField(db_column='Ordercode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    orderstyle = models.CharField(db_column='Orderstyle', max_length=20)  # Field name made lowercase.
    contcode = models.CharField(db_column='Contcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=10)  # Field name made lowercase.
    inprice_tax = models.DecimalField(db_column='Inprice_Tax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    seenum = models.DecimalField(db_column='Seenum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bill_in'
        unique_together = (('code', 'grpcode', 'shopcode', 'spercode', 'chdate', 'orderstyle'),)
        ordering = ['-chdate']


class BillInd(models.Model):
    code = models.CharField(db_column='Code', max_length=20)  # Field name made lowercase.
    rid = models.CharField(db_column='Rid', max_length=20)  # Field name made lowercase.
    procode = models.CharField(db_column='Procode', max_length=20)  # Field name made lowercase.
    salebn = models.CharField(db_column='Salebn', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pname = models.CharField(db_column='Pname', max_length=64, blank=True, null=True)  # Field name made lowercase.
    classes = models.CharField(db_column='Classes', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num = models.DecimalField(db_column='Num', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    innums = models.DecimalField(db_column='Innums', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    denums = models.DecimalField(db_column='Denums', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    giftnum = models.DecimalField(db_column='Giftnum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='Taxrate', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    price_intax = models.DecimalField(db_column='Price_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    chdate = models.DateTimeField(db_column='Chdate',auto_now_add=True)  # Field name made lowercase.
    prnum = models.DecimalField(db_column='Prnum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sum_tax = models.DecimalField(db_column='Sum_Tax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sum = models.DecimalField(db_column='Sum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rowno = models.IntegerField(db_column='Rowno')  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=10)  # Field name made lowercase.
    orderstyle = models.CharField(db_column='Orderstyle', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bill_ind'


class Billhead0(models.Model):
    sheetid = models.CharField(db_column='SheetID', primary_key=True, max_length=16)  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    payablemoney = models.DecimalField(db_column='PayableMoney', max_digits=14, decimal_places=4)  # Field name made lowercase.
    kxmoney = models.DecimalField(db_column='KXMoney', max_digits=12, decimal_places=2)  # Field name made lowercase.
    kxcash = models.DecimalField(db_column='KXCash', max_digits=12, decimal_places=2)  # Field name made lowercase.
    kxinvoice = models.DecimalField(db_column='KXInVoice', max_digits=12, decimal_places=2)  # Field name made lowercase.
    payableamt = models.DecimalField(db_column='PayableAmt', max_digits=12, decimal_places=2)  # Field name made lowercase.
    closevalue = models.DecimalField(db_column='CloseValue', max_digits=12, decimal_places=2)  # Field name made lowercase.
    unjsvalue = models.DecimalField(db_column="unjsvalue",max_digits=12, decimal_places=2)
    undqvalue = models.DecimalField(db_column="undqvalue",max_digits=12, decimal_places=2)
    havinvoice = models.SmallIntegerField(db_column='HavInVoice')  # Field name made lowercase.
    flag = models.SmallIntegerField(db_column='Flag')  # Field name made lowercase.
    paytype = models.SmallIntegerField(db_column='PayType')  # Field name made lowercase.
    begindate = models.DateTimeField(db_column='BeginDate',auto_now_add=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate',auto_now_add=True)  # Field name made lowercase.
    planpaydate = models.DateTimeField(db_column='PlanPayDate',auto_now_add=True)  # Field name made lowercase.
    editor = models.CharField(db_column='Editor', max_length=8)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate',auto_now_add=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=8)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    paychecker = models.CharField(db_column='PayChecker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    paycheckdate = models.DateTimeField(db_column='PayCheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    receiver = models.CharField(db_column='Receiver', max_length=8, blank=True, null=True)  # Field name made lowercase.
    receivdate = models.DateTimeField(db_column='ReceivDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    payer = models.CharField(db_column='Payer', max_length=8, blank=True, null=True)  # Field name made lowercase.
    paydate = models.DateTimeField(db_column='PayDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    payamt = models.DecimalField(db_column='PayAmt', max_digits=12, decimal_places=2)  # Field name made lowercase.
    paytaxamt17 = models.DecimalField(db_column='PayTaxAmt17', max_digits=12, decimal_places=2)  # Field name made lowercase.
    paytaxamt13 = models.DecimalField(db_column='PayTaxAmt13', max_digits=12, decimal_places=2)  # Field name made lowercase.
    paytaxamt6 = models.DecimalField(db_column='PayTaxAmt6', max_digits=12, decimal_places=2)  # Field name made lowercase.
    paytaxamt4 = models.DecimalField(db_column='PayTaxAmt4', max_digits=12, decimal_places=2)  # Field name made lowercase.
    printcount = models.IntegerField(db_column='PrintCount')  # Field name made lowercase.
    fprintcount = models.IntegerField(db_column='FPrintCount')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bankid = models.CharField(db_column='bankID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    openmoney = models.DecimalField(db_column='OpenMoney', max_digits=12, decimal_places=2)  # Field name made lowercase.
    closemoney = models.CharField(db_column='CloseMoney', max_length=12)  # Field name made lowercase.
    bankvalue = models.CharField(db_column="bankvalue",max_length=20)
    advance =  models.DecimalField(db_column='Advance', max_digits=14, decimal_places=4)  # Field name made lowercase.
    seenum = models.IntegerField(db_column='Seenum',blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=6, default="N")
    grpcode = models.CharField(db_column='Grpcode', max_length=10, blank=True, null=True)
    contracttype = models.CharField(db_column='Contracttype', max_length=2, blank=True, null=True)
    concode = models.CharField(db_column='Concode', max_length=20, blank=True, null=True)
    vendername = models.CharField(db_column='Vendername', max_length=64, blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=64, blank=True, null=True)
    printnum = models.IntegerField(db_column='Printnum',blank=True, null=True)
    premoney = models.DecimalField(db_column='PreMoney', max_digits=14, decimal_places=4)
    curdxvalue = models.CharField(db_column='CurDXValue', max_length=12)  # Field name made lowercase.
    curdxdiffvalue = models.CharField(db_column='CurDXDiffValue', max_length=12)  # Field name made lowercase.
    beginsdate = models.DateTimeField(db_column='BeginSDate',auto_now_add=True)  # Field name made lowercase.
    endsdate = models.DateTimeField(db_column='EndSDate',auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'billhead0'


class Billheadcust(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    custid = models.CharField(db_column='custID', max_length=4)  # 关键字需要改名
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=12, decimal_places=2)  # Field name made lowercase.
    lastcustvalue = models.DecimalField(db_column='LastCustValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    receiptvalue = models.DecimalField(db_column='ReceiptValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    incostvalue = models.DecimalField(db_column='InCostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    outcostvalue = models.DecimalField(db_column='OutCostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    retcostvalue = models.DecimalField(db_column='RetCostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    balancevalue = models.DecimalField(db_column='BalanceValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    kxvalue = models.DecimalField(db_column='KXValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ecostvalue = models.DecimalField(db_column='ECostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    advisecostvalue = models.DecimalField(db_column='AdviseCostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    costvalue = models.DecimalField(db_column='CostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    costtaxvalue = models.DecimalField(db_column='CostTaxValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    currcustvalue = models.DecimalField(db_column='CurrCustValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID', blank=True, null=True)  # Field name made lowercase.
    acceptcostvalue = models.DecimalField(db_column='AcceptCostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'billheadcust'
        unique_together = (('sheetid', 'id', 'taxrate'),)


class Billheaditem0(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    paytypesortid = models.CharField(db_column='PayTypeSortID', max_length=1)  # Field name made lowercase.
    payabledate = models.DateTimeField(db_column='PayableDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    refsheetid = models.CharField(db_column='RefSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    refsheettype = models.IntegerField(db_column='RefSheetType', blank=True, null=True)  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID')  # Field name made lowercase.
    fromshopid = models.CharField(db_column='FromShopID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    inshopid = models.CharField(db_column='InShopID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    costvalue = models.DecimalField(db_column='CostValue', max_digits=14, decimal_places=0)  # Field name made lowercase.
    costtaxvalue = models.DecimalField(db_column='CostTaxValue', max_digits=14, decimal_places=0)  # Field name made lowercase.
    costtaxrate = models.DecimalField(db_column='CostTaxRate', max_digits=4, decimal_places=0)  # Field name made lowercase.
    agroflag = models.IntegerField(db_column='AgroFlag', blank=True, null=True)  # Field name made lowercase.
    salevalue = models.DecimalField(db_column='SaleValue', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    invoicesheetid = models.CharField(db_column='InvoiceSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    dkrate = models.DecimalField(db_column='DKRate', max_digits=5, decimal_places=0)  # Field name made lowercase.
    jdate = models.DateTimeField(db_column='JDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    standvalue = models.DecimalField(db_column='StandValue', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    closevalue = models.DecimalField(db_column='CloseValue', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fromsurplusid = models.IntegerField(db_column='FromSurplusID', blank=True, null=True)  # Field name made lowercase.
    tosurplusid = models.IntegerField(db_column='ToSurplusID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'billheaditem0'


class Billheadkxitem0(models.Model):
    serialid = models.IntegerField(db_column='SerialID')  # Field name made lowercase.
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    kno = models.IntegerField(db_column="kno")
    ktype = models.IntegerField(db_column='Ktype')  # Field name made lowercase.
    payabledate = models.DateTimeField(db_column='PayableDate',auto_now_add=True)  # Field name made lowercase.
    fromshopid = models.CharField(db_column='FromShopID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    inshopid = models.CharField(db_column='InShopID', max_length=4)  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID', blank=True, null=True)  # Field name made lowercase.
    kmoney = models.DecimalField(db_column="kmoney",max_digits=12, decimal_places=2)
    kkflag = models.SmallIntegerField(db_column="kkflag")
    style = models.IntegerField(db_column='Style')  # Field name made lowercase.
    monthid = models.IntegerField(db_column='MonthID')  # Field name made lowercase.
    receiptid = models.CharField(db_column='ReceiptID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column="note",max_length=64, blank=True, null=True)
    consume = models.DecimalField(db_column="consume",max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'billheadkxitem0'
        unique_together = (('serialid', 'sheetid'),)


class Cost(models.Model):
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    contractcost = models.DecimalField(db_column='ContractCost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    costtaxrate = models.DecimalField(db_column='CostTaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    rebaterate = models.DecimalField(db_column='RebateRate', max_digits=5, decimal_places=2)  # Field name made lowercase.
    dkrate = models.DecimalField(db_column='DKRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    promflag = models.IntegerField(db_column='PromFlag')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    clearflag = models.IntegerField(db_column='ClearFlag')  # Field name made lowercase.
    cleardate = models.DateTimeField(db_column='ClearDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    basecost = models.DecimalField(db_column='BaseCost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    contractenddate = models.DateTimeField(db_column='ContractEndDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cost'
        unique_together = (('goodsid', 'shopid', 'venderid'),)


class Dept(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=32)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    marginrate = models.DecimalField(db_column='MarginRate', max_digits=5, decimal_places=2)  # Field name made lowercase.
    auditflag = models.IntegerField(db_column='AuditFlag')  # Field name made lowercase.
    orderflag = models.IntegerField(db_column="orderflag")
    needpurchase = models.IntegerField(db_column='NeedPurchase')  # Field name made lowercase.
    modifycost = models.IntegerField(db_column='ModifyCost')  # Field name made lowercase.
    highstockdays = models.IntegerField(db_column='HighStockDays')  # Field name made lowercase.
    lowstockdays = models.IntegerField(db_column='LowStockDays')  # Field name made lowercase.
    plansku = models.IntegerField(db_column='PlanSKU')  # Field name made lowercase.
    clearflag = models.IntegerField(db_column='Clearflag')  # Field name made lowercase.
    cleardate = models.DateTimeField(db_column='Cleardate',auto_now_add=True)  # Field name made lowercase.
    runtype = models.IntegerField(db_column='RunType')  # Field name made lowercase.
    accurate = models.DecimalField(db_column='AccuRate', max_digits=12, decimal_places=4)  # Field name made lowercase.
    trydays = models.IntegerField(db_column='TryDays')  # Field name made lowercase.
    trysalevalue = models.DecimalField(db_column='TrySaleValue', max_digits=12, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dept'


class Deptlevel(models.Model):
    deptlevelid = models.IntegerField(db_column='DeptLevelID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=16)  # Field name made lowercase.
    levelvalue = models.IntegerField(db_column='LevelValue')  # Field name made lowercase.
    levelwidth = models.IntegerField(db_column='LevelWidth')  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'deptlevel'


class DjangoSession(models.Model):
    session_key = models.CharField(db_column="session_key",primary_key=True, max_length=40)
    session_data = models.TextField(db_column="session_data")
    expire_date = models.DateTimeField(db_column="expire_date",auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'django_session'


class Goodsshop(models.Model):
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    normalprice = models.DecimalField(db_column='NormalPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    logistics = models.IntegerField(db_column='Logistics')  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    promotiontype = models.CharField(db_column='PromotionType', max_length=1)  # Field name made lowercase.
    goodsrigh = models.IntegerField(db_column='GoodsRigh')  # Field name made lowercase.
    priceflag = models.IntegerField(db_column='PriceFlag')  # Field name made lowercase.
    costflag = models.IntegerField(db_column='CostFlag')  # Field name made lowercase.
    top1000 = models.IntegerField(db_column='Top1000')  # Field name made lowercase.
    outdate = models.DateTimeField(db_column="outdate",blank=True, null=True,auto_now_add=True)
    goodsdate = models.DateTimeField(db_column='Goodsdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    noretflag = models.IntegerField(db_column="noretflag")

    class Meta:
        managed = False
        db_table = 'goodsshop'
        unique_together = (('shopid', 'goodsid'),)


class Kxd(models.Model):
    kno = models.IntegerField(db_column="kno",primary_key=True)
    kname = models.CharField(db_column="kname",max_length=64, blank=True, null=True)
    ktype = models.IntegerField(db_column="ktype")
    accno = models.CharField(db_column="accno",max_length=20)
    direction = models.IntegerField(db_column='Direction')  # Field name made lowercase.
    prtflag = models.IntegerField(db_column='Prtflag')  # Field name made lowercase.
    calcflag = models.IntegerField(db_column='CalcFlag')  # Field name made lowercase.
    feetype = models.IntegerField(db_column='FeeType')  # Field name made lowercase.
    incometype = models.IntegerField(db_column='InComeType')  # Field name made lowercase.
    rptorder = models.IntegerField(db_column='rptOrder')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'kxd'


class Kxsum(models.Model):
    serialid = models.IntegerField(db_column='SerialID', primary_key=True)  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID')  # Field name made lowercase.
    kno = models.IntegerField(db_column='Kno')  # Field name made lowercase.
    ktype = models.IntegerField(db_column='Ktype')  # Field name made lowercase.
    kmoney = models.DecimalField(db_column='Kmoney', max_digits=12, decimal_places=2)  # Field name made lowercase.
    kkflag = models.IntegerField(db_column='KKflag')  # Field name made lowercase.
    style = models.IntegerField(db_column='Style')  # Field name made lowercase.
    monthid = models.IntegerField(db_column='MonthID')  # Field name made lowercase.
    receivabledate = models.DateTimeField(db_column='ReceivableDate',auto_now_add=True)  # Field name made lowercase.
    stoppay = models.IntegerField(db_column='StopPay')  # Field name made lowercase.
    operator = models.CharField(db_column="operator",max_length=8, blank=True, null=True)
    editor = models.CharField(db_column="editor",max_length=8, blank=True, null=True)
    editdate = models.DateTimeField(db_column="editdate",auto_now_add=True)
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    billheadsheetid = models.CharField(db_column='BillheadSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jsdate = models.DateTimeField(db_column='JSDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    fromshopid = models.CharField(db_column='FromShopID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column="note",max_length=64, blank=True, null=True)
    consume = models.DecimalField(db_column="consume",max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'kxsum'


class Kxsum0(models.Model):
    serialid = models.IntegerField(db_column='SerialID', primary_key=True)  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID')  # Field name made lowercase.
    kno = models.IntegerField(db_column='Kno')  # Field name made lowercase.
    ktype = models.IntegerField(db_column='Ktype')  # Field name made lowercase.
    kmoney = models.DecimalField(db_column='Kmoney', max_digits=12, decimal_places=2)  # Field name made lowercase.
    kkflag = models.IntegerField(db_column='KKflag')  # Field name made lowercase.
    style = models.IntegerField(db_column='Style')  # Field name made lowercase.
    monthid = models.IntegerField(db_column='MonthID')  # Field name made lowercase.
    receivabledate = models.DateTimeField(db_column='ReceivableDate',auto_now_add=True)  # Field name made lowercase.
    stoppay = models.IntegerField(db_column='StopPay')  # Field name made lowercase.
    operator = models.CharField(max_length=8, blank=True, null=True)
    editor = models.CharField(max_length=8, blank=True, null=True)
    editdate = models.DateTimeField(auto_now_add=True)
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    billheadsheetid = models.CharField(db_column='BillheadSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    jsdate = models.DateTimeField(db_column='JSDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    fromshopid = models.CharField(db_column='FromShopID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(max_length=64, blank=True, null=True)
    consume = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'kxsum0'


class Ord(models.Model):
    ordercode = models.CharField(db_column='Ordercode',primary_key=True, max_length=20)  #
    purdate = models.DateTimeField(db_column='Purdate',auto_now_add=True)  # Field name made lowercase.
    chdate = models.DateTimeField(db_column='Chdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    spercode = models.CharField(db_column='Spercode', max_length=20)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=10)  # Field name made lowercase.
    sdate = models.DateTimeField(db_column='Sdate',auto_now_add=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=20, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=64, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='Checkdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    spername = models.CharField(db_column='Spername', max_length=64)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    style = models.CharField(db_column='Style', max_length=20)  # Field name made lowercase.
    concode = models.CharField(db_column='Concode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    teamcode = models.CharField(db_column='Teamcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inprice_tax = models.CharField(db_column='Inprice_Tax', max_length=18, blank=True, null=True)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=10, blank=True, null=True)  # Field name made lowercase.
    printnum = models.CharField(db_column='Printnum', max_length=18, blank=True, null=True)  # Field name made lowercase.
    seenum = models.CharField(db_column='Seenum', max_length=18, blank=True, null=True)  # Field name made lowercase.
    yyshdate = models.DateTimeField(db_column='Yyshdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    ssspzb = models.CharField(db_column='Ssspzb', max_length=18, blank=True, null=True)  # Field name made lowercase.
    update_flag = models.CharField(db_column='Update_Flag', max_length=2)  # Field name made lowercase.
    orderclass = models.CharField(db_column='Orderclass', max_length=2, blank=True, null=True)  # Field name made lowercase.
    dhshopcode = models.CharField(db_column='Dhshopcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    spsum = models.DecimalField(db_column='Spsum', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sjshsum = models.DecimalField(db_column='Sjshsum', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    purday = models.IntegerField(db_column='Purday')  # Field name made lowercase.
    inflag = models.IntegerField(db_column='InFlag')  # Field name made lowercase.
    logistics = models.IntegerField(db_column='Logistics')  # Field name made lowercase.
    scmtypeflag = models.IntegerField()
    scmpurdate = models.DateTimeField(db_column='scmPurdate',auto_now_add=True)  # Field name made lowercase.
    crreceiptflag = models.IntegerField(db_column='CRReceiptFlag')  # Field name made lowercase.
    refsheetid = models.CharField(db_column='RefSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    receiptsheetid = models.CharField(db_column='ReceiptSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ord'
        unique_together = (('ordercode', 'spercode', 'grpcode'),)


class OrdD(models.Model):
    ordercode = models.CharField(db_column='Ordercode', max_length=20)  # Field name made lowercase.
    rid = models.CharField(db_column='Rid', max_length=20)  # Field name made lowercase.
    procode = models.CharField(db_column='Procode', max_length=20)  # Field name made lowercase.
    salebn = models.CharField(db_column='Salebn', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pn = models.CharField(db_column='Pn', max_length=64, blank=True, null=True)  # Field name made lowercase.
    classes = models.CharField(db_column='Classes', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='Taxrate', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    num = models.DecimalField(db_column='Num', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    innums = models.DecimalField(db_column='Innums', max_digits=18, decimal_places=3)  # Field name made lowercase.
    denums = models.DecimalField(db_column='Denums', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    price_intax = models.DecimalField(db_column='Price_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sum_intax = models.DecimalField(db_column='Sum_Intax', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    nums_inplan = models.DecimalField(db_column='Nums_Inplan', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    date_inplan = models.DateTimeField(db_column='Date_Inplan', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='Checkdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    drrq = models.DateTimeField(db_column='Drrq', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    prnum = models.DecimalField(db_column='Prnum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rowno = models.IntegerField(db_column='Rowno', blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    sjshsum = models.DecimalField(db_column='Sjshsum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ssnumzb = models.DecimalField(db_column='Ssnumzb', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    sjprnum = models.DecimalField(db_column='Sjprnum', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    promflag = models.IntegerField()
    refsheetid = models.CharField(db_column='RefSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ord_d'


class OrdStatus(models.Model):
    ordercode = models.CharField(db_column='Ordercode',primary_key=True, max_length=20)  #
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    yyshdate = models.DateTimeField(db_column='Yyshdate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ord_status'

class Pubinfo(models.Model):
    infocode = models.CharField(db_column='InfoCode', max_length=20,primary_key=True)  # Field name made lowercase.
    infotype = models.CharField(db_column='InfoType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subtime = models.DateTimeField(db_column='SubTime', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    depart = models.CharField(db_column='Depart', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='GrpCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    accesstype = models.CharField(db_column='AccessType', max_length=20, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=20, blank=True, null=True)  # Field name made lowercase.
    usergrpcode = models.CharField(db_column='UserGrpCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    usergrpname = models.CharField(db_column='UserGrpName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    departname = models.CharField(db_column='DepartName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mailpath = models.CharField(db_column='MailPath', max_length=70, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'pubinfo'


class SaleVshopDaily(models.Model):
    sheetid = models.CharField(max_length=20)
    venderid = models.CharField(max_length=10)
    sdate = models.DateTimeField(auto_now_add=True)
    goodsid = models.IntegerField()
    shopid = models.CharField(max_length=6)
    categoryid = models.IntegerField()
    qty = models.DecimalField(max_digits=16, decimal_places=3)
    grosscostvalue = models.DecimalField(max_digits=14, decimal_places=2)
    netcostvalue = models.DecimalField(max_digits=14, decimal_places=2)
    costtaxrate = models.DecimalField(max_digits=4, decimal_places=2)
    grosssalevalue = models.DecimalField(max_digits=14, decimal_places=2)
    netsalevalue = models.DecimalField(max_digits=14, decimal_places=2)
    saletaxrate = models.DecimalField(max_digits=4, decimal_places=2)
    salecostrate = models.DecimalField(max_digits=4, decimal_places=2)
    touchtime = models.DateTimeField(auto_now_add=True)
    toucher = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'sale_vshop_daily'


class Sales2014(models.Model):
    sdate = models.DateTimeField(db_column='Sdate',auto_now_add=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=20)  # Field name made lowercase.
    pcode = models.CharField(db_column='Pcode', max_length=20)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num = models.DecimalField(db_column='Num', max_digits=18, decimal_places=3)  # Field name made lowercase.
    pname = models.CharField(db_column='Pname', max_length=64, blank=True, null=True)  # Field name made lowercase.
    svalue = models.CharField(db_column='Svalue', max_length=18, blank=True, null=True)  # Field name made lowercase.
    scname = models.CharField(db_column='Scname', max_length=60, blank=True, null=True)  # Field name made lowercase.
    fpcode = models.CharField(db_column='Fpcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supercode = models.CharField(db_column='Supercode', max_length=20)  # Field name made lowercase.
    bcname = models.CharField(db_column='Bcname', max_length=60, blank=True, null=True)  # Field name made lowercase.
    bccode = models.CharField(db_column='Bccode', max_length=20)  # Field name made lowercase.
    sccode = models.CharField(db_column='Sccode', max_length=20)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shopname = models.CharField(db_column='Shopname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grpname = models.CharField(db_column='Grpname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    classes = models.CharField(db_column='Classes', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scost = models.DecimalField(db_column='Scost', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    departcode = models.CharField(db_column='Departcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    departname = models.CharField(db_column='Departname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    teamcode = models.CharField(db_column='Teamcode', max_length=20)  # Field name made lowercase.
    teamname = models.CharField(db_column='Teamname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sdepartno = models.CharField(db_column='Sdepartno', max_length=20, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discount = models.DecimalField(db_column='Discount', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    zzk = models.DecimalField(db_column='Zzk', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=18, decimal_places=3)  # Field name made lowercase.
    sheettype = models.CharField(db_column='SheetType', max_length=255)  # Field name made lowercase.
    dkrate = models.DecimalField(db_column='DKRate', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sales2014'


class SalesPro(models.Model):
    sdate = models.DateTimeField(db_column='Sdate',auto_now_add=True)  # Field name made lowercase.
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    shopcode = models.CharField(db_column='Shopcode', max_length=20)  # Field name made lowercase.
    sstyle = models.CharField(db_column='Sstyle', max_length=20)  # Field name made lowercase.
    pcode = models.CharField(db_column='Pcode', max_length=20)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=20, blank=True, null=True)  # Field name made lowercase.
    num = models.DecimalField(db_column='Num', max_digits=18, decimal_places=3)  # Field name made lowercase.
    pname = models.CharField(db_column='Pname', max_length=64, blank=True, null=True)  # Field name made lowercase.
    svalue = models.DecimalField(db_column='Svalue', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    scname = models.CharField(db_column='Scname', max_length=60, blank=True, null=True)  # Field name made lowercase.
    fpcode = models.CharField(db_column='Fpcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supercode = models.CharField(db_column='Supercode', max_length=20)  # Field name made lowercase.
    bcname = models.CharField(db_column='Bcname', max_length=60, blank=True, null=True)  # Field name made lowercase.
    bccode = models.CharField(db_column='Bccode', max_length=20)  # Field name made lowercase.
    sccode = models.CharField(db_column='Sccode', max_length=20)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shopname = models.CharField(db_column='Shopname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grpname = models.CharField(db_column='Grpname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    classes = models.CharField(db_column='Classes', max_length=50, blank=True, null=True)  # Field name made lowercase.
    scost = models.DecimalField(db_column='Scost', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    departcode = models.CharField(db_column='Departcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    departname = models.CharField(db_column='Departname', max_length=20, blank=True, null=True)  # Field name made lowercase.
    teamcode = models.CharField(db_column='Teamcode', max_length=20)  # Field name made lowercase.
    teamname = models.CharField(db_column='Teamname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sdepartno = models.CharField(db_column='Sdepartno', max_length=20, blank=True, null=True)  # Field name made lowercase.
    barcode = models.CharField(db_column='Barcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    discount = models.DecimalField(db_column='Discount', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    zzk = models.DecimalField(db_column='Zzk', max_digits=18, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    tax = models.DecimalField(db_column='Tax', max_digits=18, decimal_places=3)  # Field name made lowercase.
    sheettype = models.IntegerField(db_column='SheetType')  # Field name made lowercase.
    dkrate = models.DecimalField(db_column='DKRate', max_digits=4, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sales_pro'


class ScmCost(models.Model):
    goodsid = models.IntegerField()
    shopid = models.CharField(max_length=4)
    venderid = models.IntegerField()
    contractcost = models.DecimalField(max_digits=12, decimal_places=4)
    cost = models.DecimalField(max_digits=12, decimal_places=4)
    costtaxrate = models.DecimalField(max_digits=4, decimal_places=2)
    rebaterate = models.DecimalField(max_digits=5, decimal_places=2)
    dkrate = models.DecimalField(max_digits=4, decimal_places=2)
    flag = models.IntegerField()
    promflag = models.IntegerField()
    startdate = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    enddate = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    clearflag = models.IntegerField()
    cleardate = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    basecost = models.DecimalField(max_digits=12, decimal_places=4)
    contractenddate = models.DateTimeField(blank=True, null=True,auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'scm_cost'
        unique_together = (('goodsid', 'shopid', 'venderid'),)


class ScmCust(models.Model):
    invoicesheetid = models.CharField(db_column='InvoiceSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    planpaydate = models.DateTimeField(db_column='PlanPayDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    billheadsheetid = models.CharField(db_column='BillheadSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    custtype = models.IntegerField(db_column='CustType')  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    cno = models.CharField(max_length=10)
    cname = models.CharField(max_length=40)
    cdno = models.CharField(max_length=15)
    cdate = models.DateTimeField(auto_now_add=True)
    cclass = models.SmallIntegerField()
    cgood = models.CharField(max_length=40)
    ctaxrate = models.DecimalField(max_digits=4, decimal_places=2)
    ctotal = models.DecimalField(max_digits=12, decimal_places=2)
    cmoney = models.DecimalField(max_digits=12, decimal_places=2)
    csh = models.DecimalField(max_digits=10, decimal_places=2)
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    updateflag = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'scm_cust'
        unique_together = (('venderid', 'cno', 'shopid'),)

class SerialNumber(models.Model):
    serialid = models.IntegerField(db_column='Serialid')
    name = models.CharField(db_column='Name',max_length=64)
    flag = models.IntegerField(db_column='Flag')
    serialnumber = models.IntegerField(db_column='SerialNumber')
    resetdate = models.DateField(db_column='ResetDate',auto_now_add=True)
    dailyreset = models.IntegerField(db_column='DailyReset')
    servertranflag = models.IntegerField(db_column='ServerTranFlag')
    sheetflag = models.IntegerField(db_column='SheetFlag')
    aftercheckmoduleid = models.CharField(db_column='AfterCheckModuleID',max_length=255)
    deptcode = models.CharField(db_column='DeptCode',max_length=6)

    class Meta:
        managed = False
        db_table = 'serialnumber'


class ScmGoods(models.Model):
    grpcode = models.CharField(db_column='Grpcode', max_length=20)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64)  # Field name made lowercase.
    unitname = models.CharField(db_column='UnitName', max_length=20)  # Field name made lowercase.
    spec = models.CharField(db_column='Spec', max_length=50, blank=True, null=True)  # Field name made lowercase.
    brandid = models.IntegerField(db_column='BrandID')  # Field name made lowercase.
    deptid = models.CharField(db_column='DeptID', max_length=50)  # Field name made lowercase.
    deptname = models.CharField(db_column='DeptName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    costtaxrate = models.DecimalField(db_column='CostTaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    dkrate = models.DecimalField(db_column='DKRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    promflag = models.IntegerField(db_column='PromFlag')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    barcodeid = models.CharField(db_column='BarcodeID', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'scm_goods'


class Sgroup(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=40)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=32, blank=True, null=True)  # Field name made lowercase.
    deptlevelid = models.IntegerField(db_column='DeptLevelID')  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    marginrate = models.DecimalField(db_column='MarginRate', max_digits=5, decimal_places=2)  # Field name made lowercase.
    auditflag = models.IntegerField(db_column='AuditFlag')  # Field name made lowercase.
    orderflag = models.IntegerField()
    needpurchase = models.IntegerField(db_column='NeedPurchase')  # Field name made lowercase.
    modifycost = models.IntegerField(db_column='ModifyCost')  # Field name made lowercase.
    highstockdays = models.IntegerField(db_column='HighStockDays')  # Field name made lowercase.
    lowstockdays = models.IntegerField(db_column='LowStockDays')  # Field name made lowercase.
    plansku = models.IntegerField(db_column='PlanSKU')  # Field name made lowercase.
    clearflag = models.IntegerField(db_column='Clearflag')  # Field name made lowercase.
    cleardate = models.DateTimeField(db_column='Cleardate',auto_now_add=True)  # Field name made lowercase.
    runtype = models.IntegerField(db_column='RunType')  # Field name made lowercase.
    trydays = models.IntegerField(db_column='TryDays')  # Field name made lowercase.
    trysalevalue = models.DecimalField(db_column='TrySaleValue', max_digits=12, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sgroup'



class Unbilldxsheet0(models.Model):
    serialid = models.IntegerField(db_column='SerialID', primary_key=True)  # Field name made lowercase.
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    sheettype = models.IntegerField(db_column='SheetType')  # Field name made lowercase.
    paytypeid = models.CharField(db_column='PayTypeID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    inoutdate = models.DateTimeField(db_column='InOutDate',auto_now_add=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate',auto_now_add=True)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    shopid2 = models.CharField(db_column='ShopID2', max_length=8, blank=True, null=True)  # Field name made lowercase.
    costvalue = models.DecimalField(db_column='CostValue', max_digits=12, decimal_places=2)  # Field name made lowercase.
    pricevalue = models.DecimalField(db_column='PriceValue', max_digits=12, decimal_places=2)  # Field name made lowercase.
    costtaxrate = models.DecimalField(db_column='CostTaxRate', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pricetaxrate = models.DecimalField(db_column='PriceTaxRate', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    costtaxvalue = models.DecimalField(db_column='CostTaxValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pricetaxvalue = models.DecimalField(db_column='PriceTaxValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    billheadsheetid = models.CharField(db_column='BillHeadSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField()
    note = models.CharField(db_column='Note', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'unbilldxsheet0'


class Updcostvalue(models.Model):
    sheetid = models.CharField(db_column='SheetID', primary_key=True, max_length=16)  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    rundate = models.DateTimeField(db_column='RunDate',auto_now_add=True)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    updatemode = models.IntegerField(db_column='UpdateMode')  # Field name made lowercase.
    venderpayableflag = models.IntegerField(db_column='VenderPayableFlag')  # Field name made lowercase.
    refsheetid = models.CharField(db_column='RefSheetID', max_length=16, blank=True, null=True)  # Field name made lowercase.
    refsheettype = models.IntegerField(db_column='RefSheetType', blank=True, null=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=64, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    editor = models.CharField(db_column='Editor', max_length=8)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate',auto_now_add=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updcostvalue'


class Updcostvaluecostitem(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    goodscostid = models.IntegerField(db_column='GoodsCostID')  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    oldcost = models.DecimalField(db_column='OldCost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    paytypeid = models.CharField(db_column='PayTypeID', max_length=2)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=12, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updcostvaluecostitem'


class Updcostvalueitem(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    goodscostid = models.IntegerField(db_column='GoodsCostID')  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    oldcost = models.DecimalField(db_column='OldCost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    newcost = models.DecimalField(db_column='NewCost', max_digits=12, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    costvalue = models.DecimalField(db_column='CostValue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updcostvalueitem'
        unique_together = (('sheetid', 'goodscostid', 'goodsid', 'oldcost'),)


class Updgoodscost(models.Model):
    sheetid = models.CharField(db_column='SheetID', primary_key=True, max_length=16)  # Field name made lowercase.
    venderpayableflag = models.IntegerField(db_column='VenderPayableFlag')  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=64, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    editor = models.CharField(db_column='Editor', max_length=8)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate',auto_now_add=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID')  # Field name made lowercase.
    printcount = models.IntegerField(db_column='PrintCount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updgoodscost'


class Updgoodscostitem(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    goodscostid = models.IntegerField(db_column='GoodsCostID')  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    paytypeid = models.CharField(db_column='PayTypeID', max_length=2)  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=12, decimal_places=0)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='Taxrate', max_digits=4, decimal_places=0)  # Field name made lowercase.
    oldqty = models.DecimalField(db_column='OldQty', max_digits=12, decimal_places=0)  # Field name made lowercase.
    adjustqty = models.DecimalField(db_column='AdjustQty', max_digits=12, decimal_places=0)  # Field name made lowercase.
    placeid = models.IntegerField(db_column='PlaceID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updgoodscostitem'
        unique_together = (('sheetid', 'goodscostid'),)


class Updpayable(models.Model):
    sheetid = models.CharField(db_column='SheetID', primary_key=True, max_length=16)  # Field name made lowercase.
    refsheetid = models.CharField(db_column='RefSheetID', max_length=16)  # Field name made lowercase.
    refsheettype = models.IntegerField(db_column='RefSheetType')  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    venderid = models.IntegerField(db_column='VenderID')  # Field name made lowercase.
    refcheckdate = models.DateTimeField(db_column='RefCheckDate',auto_now_add=True)  # Field name made lowercase.
    note = models.CharField(db_column='Note', max_length=64, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    editor = models.CharField(db_column='Editor', max_length=8)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate',auto_now_add=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updpayable'


class Updpayableitem(models.Model):
    serialid = models.IntegerField(db_column='SerialID', primary_key=True)  # Field name made lowercase.
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    paytypeid = models.CharField(db_column='PayTypeID', max_length=2)  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    costvalue = models.DecimalField(db_column='CostValue', max_digits=12, decimal_places=0)  # Field name made lowercase.
    costtaxrate = models.DecimalField(db_column='CostTaxRate', max_digits=4, decimal_places=0)  # Field name made lowercase.
    costtaxvalue = models.DecimalField(db_column='CostTaxValue', max_digits=12, decimal_places=0)  # Field name made lowercase.
    agroflag = models.IntegerField(db_column='AgroFlag')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'updpayableitem'


class Vstocktrans(models.Model):
    sheetid = models.CharField(db_column='SheetID', primary_key=True, max_length=16)  # Field name made lowercase.
    shopid = models.CharField(db_column='ShopID', max_length=4)  # Field name made lowercase.
    managedeptid = models.IntegerField(db_column='ManageDeptID')  # Field name made lowercase.
    outvenderid = models.IntegerField(db_column='OutVenderID')  # Field name made lowercase.
    invenderid = models.IntegerField(db_column='InVenderID')  # Field name made lowercase.
    transfermethod = models.IntegerField(db_column='TransferMethod')  # Field name made lowercase.
    tflag = models.SmallIntegerField(db_column='TFlag')  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag')  # Field name made lowercase.
    editor = models.CharField(db_column='Editor', max_length=8)  # Field name made lowercase.
    editdate = models.DateTimeField(db_column='EditDate',auto_now_add=True)  # Field name made lowercase.
    operator = models.CharField(db_column='Operator', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checker = models.CharField(db_column='Checker', max_length=8, blank=True, null=True)  # Field name made lowercase.
    checkdate = models.DateTimeField(db_column='CheckDate', blank=True, null=True,auto_now_add=True)  # Field name made lowercase.
    note = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vstocktrans'


class Vstocktranscostitem(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    deptid = models.IntegerField(db_column='DeptID')  # Field name made lowercase.
    outgoodscostid = models.IntegerField(db_column='OutGoodsCostID')  # Field name made lowercase.
    outpaytypeid = models.CharField(db_column='OutPayTypeID', max_length=2)  # Field name made lowercase.
    ingoodscostid = models.IntegerField(db_column='InGoodsCostID')  # Field name made lowercase.
    inpaytypeid = models.CharField(db_column='InPayTypeID', max_length=2)  # Field name made lowercase.
    planqty = models.DecimalField(db_column='PlanQty', max_digits=12, decimal_places=3)  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=12, decimal_places=3)  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=12, decimal_places=4)  # Field name made lowercase.
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=4, decimal_places=2)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vstocktranscostitem'
        unique_together = (('sheetid', 'goodsid', 'outgoodscostid'),)


class Vstocktransitem(models.Model):
    sheetid = models.CharField(db_column='SheetID', max_length=16)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID')  # Field name made lowercase.
    goodscostid = models.IntegerField(db_column='GoodsCostID')  # Field name made lowercase.
    qty = models.DecimalField(db_column='Qty', max_digits=12, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vstocktransitem'
        unique_together = (('sheetid', 'goodsid', 'goodscostid'),)

class Reconcil(models.Model):
    rname = models.CharField(db_column='rname',max_length=20)
    status = models.CharField(db_column='status',max_length=2)
    beginday = models.IntegerField(db_column='beginday')
    endday = models.IntegerField(db_column='endday')
    class Meta:
        managed = False
        db_table = 'reconcil'

class ReconcilItem(models.Model):
    rid = models.IntegerField(db_column='rid')
    pid = models.CharField(db_column='pid',max_length=2)

    class Meta:
        managed = False
        db_table = 'reconcilitem'

class BasPayType(models.Model):
    id = models.CharField(db_column='Id',max_length=2,primary_key=True)
    name = models.CharField(db_column='Name',max_length=16)
    paytypesortid = models.CharField(db_column='PayTypeSortID',max_length=1)
    paytypeday = models.IntegerField(db_column='PayTypeDay')
    style = models.IntegerField(db_column='Style')
    pri = models.IntegerField(db_column='PRI')
    runtype = models.IntegerField(db_column='RunType')
    dkflag = models.IntegerField(db_column='DkFlag')

    class Meta:
        managed = False
        db_table = 'bas_paytype'

class RepShopZeroStock(models.Model):
    shopid = models.CharField(db_column='ShopID',max_length=16)
    shopname = models.CharField(db_column='ShopName',max_length=100)
    deptid = models.CharField(db_column='DeptId',max_length=16)
    deptname = models.CharField(db_column='DeptName',max_length=100)
    qtyz = models.DecimalField(db_column='Qtyz', max_digits=16, decimal_places=2)
    qtyl = models.DecimalField(db_column='Qtyl', max_digits=16, decimal_places=2)
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'rep_shopzerostock'

class RepShopNegativeStock(models.Model):
    shopid = models.CharField(db_column='ShopID',max_length=16)
    shopname = models.CharField(db_column='ShopName',max_length=100)
    deptid = models.CharField(db_column='DeptId',max_length=16)
    deptname = models.CharField(db_column='DeptName',max_length=100)
    qtyz = models.DecimalField(db_column='Qtyz', max_digits=16, decimal_places=2)
    qtyl = models.DecimalField(db_column='Qtyl', max_digits=16, decimal_places=2)
    createtime = models.DateTimeField(db_column='CreateTime',auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'rep_shopnegativestock'


class KgNegStock(models.Model):
    shopid = models.CharField(max_length=4, blank=True, null=True)
    shopname = models.CharField(max_length=64, blank=True, null=True)
    sgroupid = models.IntegerField(db_column='sGroupID', blank=True, null=True)  # Field name made lowercase.
    sgroupname = models.CharField(db_column='sGroupName', max_length=16, blank=True, null=True)  # Field name made lowercase.
    goodsid = models.IntegerField(db_column='GoodsID', blank=True, null=True)  # Field name made lowercase.
    goodsname = models.CharField(db_column='GoodsName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(max_digits=16, decimal_places=4, blank=True, null=True)
    costvalue = models.DecimalField(db_column='CostValue', max_digits=16, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='Spec', max_length=16, blank=True, null=True)  # Field name made lowercase.
    unitname = models.CharField(db_column='UnitName', max_length=8, blank=True, null=True)  # Field name made lowercase.
    deptid = models.IntegerField(blank=True, null=True)
    deptname = models.CharField(max_length=64, blank=True, null=True)
    venderid = models.IntegerField(db_column='Venderid', blank=True, null=True)  # Field name made lowercase.
    vendername = models.CharField(db_column='VenderName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    promflag = models.IntegerField(db_column='Promflag', blank=True, null=True)  # Field name made lowercase.
    openqty = models.DecimalField(db_column='OpenQty', max_digits=16, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    receiptdate = models.DateTimeField(db_column='ReceiptDate', blank=True, null=True)  # Field name made lowercase.
    onreceiptqty = models.DecimalField(db_column='OnReceiptQty', max_digits=16, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    saledate = models.DateTimeField(db_column='SaleDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KGnegstock'
