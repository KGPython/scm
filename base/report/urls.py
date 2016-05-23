#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.conf.urls import url

urlpatterns = [
    #零库存排名
    url(r'^report/daily/zerostock/index/','base.report.daily.zerostocktop.index',name='zeroStockTopIndex'),
    url(r'^report/daily/zerostock/query/','base.report.daily.zerostocktop.query',name='zeroStockTopQuery'),
    url(r'^report/daily/zerostock/download/','base.report.daily.zerostocktop.download',name='zeroStockTopDownload'),
    #负库存排名
    url(r'^report/daily/negativestock/index/','base.report.daily.negativestocktop.index',name='negativeStockTopIndex'),
    url(r'^report/daily/negativestock/query/','base.report.daily.negativestocktop.query',name='negativeStockTopQuery'),
    url(r'^report/daily/negativestock/download/','base.report.daily.negativestocktop.download',name='negativeStockTopDownload'),

    #集团营运日报表
    url(r'^report/daily/grpoperate/index/','base.report.daily.group_operate.index',name='grpOperateIndex'),
    url(r'^report/daily/grpoperate/query/','base.report.daily.group_operate.query',name='grpOperateQuery'),
    url(r'^report/daily/grpoperate/download/','base.report.daily.group_operate.download',name='grpOperateDownload'),
]