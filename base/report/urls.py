#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.conf.urls import url

urlpatterns = [
    #负库存排名
    url(r'^report/daily/negativestock/index/','base.report.daily.negativestocktop.index',name='negativeStockTopIndex'),
    # url(r'^report/daily/negativestock/query/','base.report.daily.negativestocktop.query',name='negativeStockTopQuery'),
    # url(r'^report/daily/negativestock/download/','base.report.daily.negativestocktop.download',name='negativeStockTopDownload'),
    #负库存课组明细
    url(r'^report/daily/negStockDeptDetail/$','base.report.daily.negStockDeptDetail.index',name='negStockDeptDetail'),
    #负库存课组汇总
    url(r'^report/daily/negStockDept/$','base.report.daily.negStockDept.index',name='negStockDept'),

    #零库存排名
    url(r'^report/daily/zeroStockTop/$','base.report.daily.zerostocktop.index',name='zeroStockTop'),
    url(r'^report/daily/zeroStockDept/$','base.report.daily.zeroStockDept.index',name='zeroStockDept'),
    #集团营运日报表
    url(r'^report/daily/grpoperate/index/$','base.report.daily.group_operate.index',name='grpOperateIndex'),
    url(r'^report/daily/grpgeneralopt/index/$','base.report.daily.group_general_operate.index',name='grpGenOptIndex'),
    url(r'^report/daily/grpcvsopt/index/$','base.report.daily.group_cvs_operate.index',name='grpCvsOptIndex'),
    url(r'^report/daily/grpsale/index/$','base.report.daily.group_sale.index',name='grpSaleIndex'),
    url(r'^report/daily/grpoptdecmpt/index/$','base.report.daily.group_operate_decompt.index',name='grpGptDecmptIndex'),
    # 各课组门店销售前十
    url(r'^report/daily/saletop10/index/', 'base.report.daily.saletop10.index', name='saletop10Index'),

]