#-*- coding:utf-8 -*-
__author__ = 'liubf'

#协同信息类型
PUBINFO_TYPE = {"0":"系统公告","1":"供应商通知","2":"促销动态","3":"新品发布","4":"招商引店"}

#用户类型
USER_TYPE = {"0":"平台", "1":"集团", "2":"供应商"}

#订单状态
ORG_STATUS = {"0":"有效","1":"无效"}

PROM_FLAG = {"0":"正常","1":"促销"}

PWD_PREFIX = "www.ikuanguang.com"

SALE_STATUS = {"0":"正常","1":"暂停订货","2":"暂停销售","3":"已清退","4":"清退","5":"暂停经营","6":"待清退","7":"待启用","8":"新品"}

FONT_ARIAL = "/static/css/data/Arial.ttf"
WORD_DATA="/static/css/data/word.data"

#供应商Home页地址
URL_SUPPLIER_HOME = "/scm/base/supp/home/"
#零售商Home页地址
URL_RETAILER_HOME = "/scm/base/admin/index/"

BASE_ROOT = "/home/system/djangoapps/scm"

ERP_START_TIME = [2012,1,1]

SCM_ACCOUNT_USER_NAME = "网上对账"
SCM_ACCOUNT_LOGINID = "9999"
SCM_ACCOUNT_WORKSTATIONID = 1
SCM_ACCOUNT_MODULEID = "999901"
#事件代码 （88001-88099）
# 88001-88005 结算申请单
# 88001-新建，88002-修改，88003-删除
#
# 88006-88010 发票接收单
# 88006-新建，88007-修改，88008-删除
SCM_ACCOUNT_EVENTID =["88001","88002","88003","88004","88005","88006","88007","88008"]
