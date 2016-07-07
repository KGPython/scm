#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.conf.urls import url

urlpatterns = [
    #负库存排名
    url(r'^report/daily/negativestock/index/','base.report.daily.negativestocktop.index',name='negativeStockTopIndex'),
    # url(r'^report/daily/negativestock/query/','base.report.daily.negativestocktop.query',name='negativeStockTopQuery'),
    # url(r'^report/daily/negativestock/download/','base.report.daily.negativestocktop.download',name='negativeStockTopDownload'),
    #负库存课组明细
    # url(r'^report/daily/negStockDeptDetail/$','base.report.daily.negStockDeptDetail.index',name='negStockDeptDetail'),
    #负库存课组汇总
    # url(r'^report/daily/negStockDept/$','base.report.daily.negStockDept.index',name='negStockDept'),

    #零库存排名
    url(r'^report/daily/zeroStockTop/$','base.report.daily.zerostocktop.index',name='zeroStockTop'),
    # url(r'^report/daily/zeroStockDept/$','base.report.daily.zeroStockDept.index',name='zeroStockDept'),
    #集团营运日报表
    url(r'^report/daily/grpoperate/index/$','base.report.daily.group_operate.index',name='grpOperateIndex'),
    url(r'^report/daily/grpgeneralopt/index/$','base.report.daily.group_general_operate.index',name='grpGenOptIndex'),
    url(r'^report/daily/grpcvsopt/index/$','base.report.daily.group_cvs_operate.index',name='grpCvsOptIndex'),
    url(r'^report/daily/grpsale/index/$','base.report.daily.group_sale.index',name='grpSaleIndex'),
    url(r'^report/daily/grpoptdecmpt/index/$','base.report.daily.group_operate_decompt.index',name='grpGptDecmptIndex'),
    #异常数据
    url(r'^report/abnormal/negprofit/index/$', 'base.report.abnormal.negprofit_past3days.index', name='negProfitPast3days'),
    url(r'^report/abnormal/negprofit/lte200/$', 'base.report.abnormal.negprofit_lte200.index', name='negProfitLte200'),
    url(r'^report/abnormal/neg/negstock/$', 'base.report.abnormal.negstock.index', name='negStock'),
    # 各课组门店销售前十
    url(r'^report/daily/saletop10/index/', 'base.report.daily.saletop10.index', name='saletop10Index'),
    # 门店供应商退货率
    url(r'^report/daily/suppret/index/', 'base.report.daily.supplier_returns.index', name='supplierReturnsIndex'),
    # 门店顾客退货率
    url(r'^report/daily/custret/index/', 'base.report.daily.customer_returns.index', name='customerReturnsIndex'),
    #散装破损率
    url(r'^report/daily/bulkLost/$','base.report.daily.bulkLost.inidex',name='bulkLost'),
    #蔬菜破损率
    url(r'^report/daily/vegetableLost/$','base.report.daily.vegetableLost.inidex',name='vegetableLost'),
    #水果破损率
    url(r'^report/daily/fruitLost/$','base.report.daily.fruitLost.inidex',name='fruitLost'),

]