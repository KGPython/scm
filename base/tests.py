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

from base.utils import MethodUtil as mdu,DateUtil
import pylab


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
    print(DateUtil.get_firstday_month(-2))
    print(DateUtil.get_lastday_month(-2))
    print("月结30天" in "")






