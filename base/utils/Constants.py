#-*- coding:utf-8 -*-
__author__ = 'liubf'

#协同信息类型
PUBINFO_TYPE = {"0":"系统公告","1":"供应商通知","2":"促销动态","3":"新品发布","4":"招商引店"}

#用户类型
USER_TYPE = {"0":"平台", "1":"集团", "2":"供应商"}

#订单状态
ORG_STATUS = {"0":"有效","1":"无效"}

PROM_FLAG = {"0":"正常","1":"促销"}

USER_STATUS = {"Y":"已启用","N":"已禁用"}

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
SCM_ACCOUNT_LOGINNO = "467"
SCM_ACCOUNT_WORKSTATIONID = 1
SCM_ACCOUNT_MODULEID = "999901"
#事件代码 （88001-88099）
# 88001-88005 结算申请单
# 88001-新建，88002-修改，88003-删除
#
# 88006-88010 发票接收单
# 88006-新建，88007-修改，88008-删除
#发票流水(sheetflow)：88010-新建
SCM_ACCOUNT_EVENTID =["88001","88002","88003","88004","88005","88006","88007","88008","88010"]


SCM_UNIT = {"00069":"宽广超市集团","69":"宽广超市集团"}

CONTRACT_TYPE_DICT = {"g":"购销","d":"代销","l":"联营","z":"租赁"}

SCM_BALANCE_ID='CM01'
SCM_BALANCE_NAME='宽广超市业务中心'

SCM_SHEET_TYPE={"2301":"RK","2323":"RT","2430":"KCJJ","2431":"KCJJ","2446":"PCSL","2460":"PCZY"}

SCM_CONFIG_MODULE = "system"
SCM_CONFIG_BILL_ISLIMIT = "scm.bill.islimit"

#数据库
###正式库###
# SCM_DB_SERVER = "192.168.250.11"
# SCM_DB_PORT = 1433
# SCM_DB_USER = "scm"
# SCM_DB_PASSWORD = "Scm20140607PI"
# SCM_DB_DATABASE = "myshopcmstock"
###测试库###
SCM_DB_SERVER = "192.168.122.141"
SCM_DB_PORT = 1433
SCM_DB_USER = "myshop"
SCM_DB_PASSWORD = "oyf20140208HH"
SCM_DB_DATABASE = "mySHOPCMStock"





