"""scm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
#-*- coding:utf-8 -*-
from django.conf.urls import include,url

urlpatterns = [
	url(r'^base/index/','base.views.index'),
    url(r'^base/loginpage/', 'base.login.views.loginPage'),
    url(r'^base/login/', 'base.login.views.login'),
    url(r'^base/logout/', 'base.login.views.logout'),
    url(r'^base/vcode/', 'base.login.views.vcode'),
    url(r'^base/menu/', 'base.login.views.menu'),
    url(r'^base/updatepwd/','base.login.views.uppwd'),

    #供应商》首页
    url(r'^base/supp/home/','base.supplier.home.index'),
    url(r'^base/supp/repwd/','base.supplier.home.repwd'),

    #供应商》基本资料
    url(r'^base/supp/goods/index/','base.supplier.basic.views.index'),
    url(r'^base/supp/goods/query/','base.supplier.basic.views.query'),
    #供应商》订单
    url(r'^base/supp/order/index/','base.supplier.order.views.index'),
    url(r'^base/supp/order/query/','base.supplier.order.views.query'),
    url(r'^base/supp/order/find/','base.supplier.order.views.find'),
    url(r'^base/supp/order/save/','base.supplier.order.views.save'),
    url(r'^base/supp/order/upprint/','base.supplier.order.views.upprint'),
    #供应商》销售
    ##类别销售汇总
    url(r'^base/supp/sale/category/query/','base.supplier.sales.category.query'),
    url(r'^base/supp/sale/category/detail/','base.supplier.sales.category.detail'),
    ##单品销售列表
    url(r'^base/supp/sale/product/query/', 'base.supplier.sales.product.query'),
    ##商品销售明细
    url(r'^base/supp/sale/sellinfo/query/', 'base.supplier.sales.sellinfo.query'),
    url(r'^base/supp/sale/sellinfo/detail/', 'base.supplier.sales.sellinfo.detail'),
    ##门店柜组销售
    url(r'^base/supp/sale/counter/index/', 'base.supplier.sales.counter.index'),
    url(r'^base/supp/sale/counter/query/', 'base.supplier.sales.counter.query'),
    url(r'^base/supp/sale/counter/detail/', 'base.supplier.sales.counter.detail'),
    ##日销售分析
    url(r'^base/supp/sale/analysis/query/', 'base.supplier.sales.analysis.query'),
    url(r'^base/supp/sale/analysis/detail1/', 'base.supplier.sales.analysis.detail1'),
    url(r'^base/supp/sale/analysis/detail2/', 'base.supplier.sales.analysis.detail2'),
    url(r'^base/supp/sale/analysis/detail3/', 'base.supplier.sales.analysis.detail3'),

    url(r'^base/admin/retuser/index/', 'base.admin.retuser.views.index'),
    url(r'^base/admin/retuser/saverole/', 'base.admin.retuser.views.saverole'),
    url(r'^base/admin/retuser/findrole/', 'base.admin.retuser.views.findrole'),
    url(r'^base/admin/retuser/repwd/','base.admin.home.repwd'),

	#供应商》库存
    url(r'^base/',include('base.supplier.stock.urls')),
	#供应商》单据
	url(r'^base/',include('base.supplier.bill.urls')),
	#供应商》结算
    url(r'^base/',include('base.supplier.balance.urls')),
	url(r'^base/',include('base.retailer.balance.urls')),
    url(r'^base/',include('base.retailer.order.urls')),
	
	url(r'^base/admin/retrole/edit','base.admin.retrole.views.roleEdit',name="roleEdit"),
    url(r'^base/admin/retrole/log','base.admin.retrole.views.log',name="retLog"),

	#供应商》通知
    url(r'^base/msg/info/','base.message.views.info'),
    url(r'^base/msg/download/','base.message.views.download'),

	url(r'^base/msg/msglist/','base.message.views.msglist',name="msglist"),
	url(r'^base/msg/msgcreate/','base.message.views.msgCreate',name="msgCreate"),
	url(r'^base/msg/msgpreview/','base.message.views.msgPreview',name="msgPreview"),

    #供应商》发票(承接结算单)
    url(r'^base/supp/invoice/$','base.supplier.invioce.views.createInvioce',name='createInvioce'),
    url(r'^base/supp/invoice/save','base.supplier.invioce.views.saveInvioce',name='saveInvioce'),
    #供应商》发票(新建)
    url(r'^base/supp/invoice/new/$','base.supplier.invioce.views.newInvoice',name='newInvoice'),
    url(r'^base/supp/invoice/new/query','base.supplier.invioce.views.queryBalance',name='queryBalance'),

	#零售商&系统管理
    url(r'^base/admin/index/','base.admin.home.index'),
    url(r'^base/admin/supprole/','base.admin.supprole.views.index'),
    url(r'^base/admin/supprole_form/','base.admin.supprole.views.add_form'),
    url(r'^base/admin/suppmanager/', 'base.admin.suppmanager.views.query_supp'),
    url(r'^base/admin/supp_updatepwd/', 'base.admin.suppmanager.views.update_pwd'),
    url(r'^base/admin/suppstatus/', 'base.admin.suppstatus.view.index'),
    url(r'^base/admin/supp_sta_form', 'base.admin.suppstatus.view.suppStatusForm'),
    url(r'^base/admin/supp_findRole', 'base.admin.suppstatus.view.findRole'),
    url(r'^base/admin/supp_addRole', 'base.admin.suppstatus.view.addRole'),
    url(r'^base/admin/supp_queryRole', 'base.admin.supprole.views.queryRole'),
    url(r'^base/admin/supp_savePur', 'base.admin.supprole.views.savePur'),
    url(r'^base/admin/reconciltype/', 'base.admin.reconcilType.views.reconcilType',name="reconciltype"),
    url(r'^base/admin/retlog/purlog', 'base.admin.retlog.views.purlog',name="retPurlog"),
    url(r'^base/admin/retlog/report', 'base.admin.retlog.views.report',name="retPurlogReport"),
    url(r'^base/admin/estimate/impt', 'base.admin.estimate.views.impt',name="retEstimateImpt"),

    #报表中心
    url(r'^base/',include('base.report.urls')),

    #欢迎页面（临时）
    url(r'^welcome/$','base.login.views.welcome'),

    #负库存
    url(r'^base/report/daily/negStock/$','base.report.daily.negativestocktop.index')
]


