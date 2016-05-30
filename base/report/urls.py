#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.conf.urls import url

urlpatterns = [
    #负库存排名
    url(r'^report/daily/negativestock/index/','base.report.daily.negativestocktop.index',name='negativeStockTopIndex'),
    url(r'^report/daily/negativestock/query/','base.report.daily.negativestocktop.query',name='negativeStockTopQuery'),
    url(r'^report/daily/negativestock/download/','base.report.daily.negativestocktop.download',name='negativeStockTopDownload'),
    #负库存课组明细
    url(r'^report/daily/negStockDeptDetail/$','base.report.daily.negStockDeptDetail.index',name='negStockDeptDetail'),
    #负库存课组汇总
    url(r'^report/daily/negStockDept/$','base.report.daily.negStockDept.index',name='negStockDept'),

    #零库存排名
    url(r'^report/daily/zreostocktop/$','base.report.daily.zerostocktop.index',name='zeroStockTop'),

    #集团营运日报表
    url(r'^report/daily/grpoperate/index/$','base.report.daily.group_operate.index',name='grpOperateIndex'),
]