#-*- coding:utf-8 -*-
"""
                       _oo0oo_
                      o8888888o
                      88" . "88
                      (| -_- |)
                      0\  =  /0
                    ___/`---'\___
                  .' \\|     | '.
                 / \\|||  :  ||| \
                / _||||| -:- |||||- \
               |   | \\\  -  / |   |
               | \_|  ''\---/''  |_/ |
               \  .-\__  '-'  ___/-. /
             ___'. .'  /--.--\  `. .'___
          ."" '<  `.___\_<|>_/___.' >' "".
         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
         \  \ `_.   \_ __\ /__ _/   .-` /  /
     =====`-.____`.___ \_____/___.-`___.-'=====
                       `=---='

     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               佛祖保佑         永无BUG
"""
from django.test import TestCase

from numpy import array
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter
import matplotlib.ticker as ticker
import decimal,time,datetime
import base.utils.MethodUtil as mdu

import pytz as tz

import dateutil, pylab,random
from pylab import *

from datetime import timedelta


from pylab import *


def test():
    x = [1,2,3,4,5,6,7,8]
    xt = ("1-12月","2-12月","3-12月","4-12月","5-12月","6-12月","7-12月","8-12月")
    y = [157.00,162.00,150.00,170.00,199.00,192.00,145.00,163.00]
    plt.plot(x,y,color="red")
    plt.xlim(0.0,8.0)# set axis limits
    plt.ylim(140.0, 200.0)
    plt.xticks(x,xt)
    plt.xlabel('月份')
    plt.ylabel('金额')

    plt.grid(True)
    plt.title('供应商日销售汇总折线图')

    plt.show()


def test2():
    today = datetime.now()
    dates = [today + timedelta(days=i) for i in range(10)]
    print(dates)
    values = [3,2,8,4,5,6,7,8,11,2]
    pylab.plot_date(pylab.date2num(dates), values, linestyle='-')
    #text(17, 277, '瞬时流量示意')
    xt = [d.strftime('%m-%d') for d in dates]
    xticks(dates,xt)
    xlabel('时间time (s)')
    ylabel('单位 (m3)')
    title('供应商日销售汇总折线图')
    grid(True)
    show()

def test1():
    a = {"a":1}
    b = [("b","0.00")]
    c = ("t",1)

    print(a.get("a"))

    if isinstance(a,dict):
        print("dict-a")

    if isinstance(b,list):
        print("list-b")

    if isinstance(c,list):
        print("list-c")

    if isinstance(c,tuple):
        print("tuple-c")

def testmssql():
    conn = mdu.getMssqlConn()
    cur = conn.cursor()
    sql = "select top 10 [ID],[Name] from [Shop]"
    cur.execute(sql)
    list = cur.fetchall()
    for row in list:
        print(row["ID"],mdu.getDBVal(row,"Name"))



if __name__ == "__main__":

    print(">>>main()")
    # s = -1832.6399999999998
    # s= "%0.2f" % s
    # print(s)
    # testmssql()
    # print(rmbupper(54322754.2))

    #tz = tz.timezone('Asia/Shanghai')
    #sh_dt = datetime.datetime.now(tz)
    #print(sh_dt)
    #test2()
    # print(datetime.datetime.today().strftime("%Y"))
    # print(datetime.datetime.today().strftime("%m"))
    # print(datetime.datetime.today().strftime("%d"))
    # list = [("2015-11-11",23.1),("2015-11-4",5.1),("2015-12-5",13.25),("2015-12-21",653.25)]
    # dict= sorted(list, key=lambda d:d[1])
    # print(dict)
    #
    # print(datetime.datetime.strptime("2015-11-11",'%Y-%m-%d').timestamp())
    # print(time.strftime('%Y-%m-%d',time.localtime(1447171200)))

    # a = arange(datetime.datetime.strptime("2015-11-01",'%Y-%m-%d').timestamp(),
    #            datetime.datetime.strptime("2015-11-30",'%Y-%m-%d').timestamp(),7*24*60*60*1000)
    # print(a)
    # b = linspace(-10,10,10)
    # print(b)
    # c = [int(i) for i in b ]
    # print(c)

    # ls = ["2","3","a"]
    # try:
    #     s_sadmin = ls.index("1")
    #     print(s_sadmin)
    # except:
    #     print(-1)
    #
    # def cutStr(str,separator):
    #     try:
    #         index = str.index(separator)
    #         return str[index+1:]
    #     except:
    #         return str
    # s = "23423sd.fsdfsdf"
    # print(cutStr(s,"."))
    # testmssql()
    # s = "where {cond1}"
    # print(s.format(cond1="1=1"))
    #
    # a =[]
    # a.append("3")
    # a.append("3")
    # a.append("2")
    # a.append("1")
    # a = list(set(a))
    # b = [{"orgcode":"1","orgname":"壹"},{"orgcode":"2","orgname":"贰"},{"orgcode":"3","orgname":"叁"},{"orgcode":"4","orgname":"肆"}]
    # mdeptNames = [x["orgname"] for x in b if x["orgcode"] in a]
    # mdeptName = ",".join(mdeptNames)
    # print(mdeptName)
    # print(str(b"\xe7\x99\xbb\xe5\xbd\x95\xe7\x94\xa8\xe6\x88\xb7\xef\xbc\x9a8340375 ","utf-8"))

    # def test():
    #     for i in range(10):
    #         if i%2==0:
    #             yield i
    # print(list(test()))
    # s = "购销月结0.1天"
    # a = "半月结"
    # if a in s:
    #     print(a)
    # now = datetime.date.today().day
    # print(type(now))
    #
    # s = 23.4
    # print("%0.0f" % s)
    # s = -2 * 4 + 3 ** 2
    # print(s)
    w = ""



