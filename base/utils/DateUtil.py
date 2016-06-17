# -*- coding: utf-8 -*-

'''获取当前日期前后N天或N月的日期'''

from time import strftime, localtime,strptime
import datetime
import calendar

year = strftime("%Y",localtime())
mon  = strftime("%m",localtime())
day  = strftime("%d",localtime())
hour = strftime("%H",localtime())
min  = strftime("%M",localtime())
sec  = strftime("%S",localtime())

def strToDate(strdate):
    if strdate:
        t = strptime(strdate,"%Y-%m-%d")
        y,m,d = t[0:3]
        return datetime.date(y,m,d)
    else:
        return None

def subtract(d1,d2):
    """计算两日期间天数差：d1 - d2 """
    d = d1 - d2
    return d.days+1

def todaystr():
    '''
    get date string, date format="YYYYMMDD"
    '''
    return datetime.date.today().strftime("%Y-%m-%d")

def datetimestr():
    '''
    get datetime,format="YYYY-MM-DD HH:MM:SS"
    '''
    return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

def get_day_of_day(n=0):
    '''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if(n<0):
        n = abs(n)
        return datetime.date.today()-datetime.timedelta(days=n)
    else:
        return datetime.date.today()+datetime.timedelta(days=n)

def get_days_of_month(year,mon):
    '''
    get days of month
    '''
    return calendar.monthrange(year, mon)[1]

def get_firstday_of_month(year,mon):
    '''
    get the first day of month
    date format = "YYYY-MM-DD"
    '''
    days="01"
    if(int(mon)<10):
        mon = "0"+str(int(mon))
    arr = (year,mon,days)
    return "-".join("%s" %i for i in arr)

def get_lastday_of_month(year,mon):
    '''
    get the last day of month
    date format = "YYYY-MM-DD"
    '''
    days=calendar.monthrange(year, mon)[1]
    mon = addzero(mon)
    arr = (year,mon,days)
    return "-".join("%s" %i for i in arr)

def get_firstday_month(n=0):
    '''
    get the first day of month from today
    n is how many months
    '''
    (y,m,d) = getyearandmonth(n)
    d = "01"
    arr = (y,m,d)
    return "-".join("%s" %i for i in arr)

def get_lastday_month(n=0):
    '''
    get the last day of month from today
    n is how many months
    '''
    return "-".join("%s" %i for i in getyearandmonth(n))

def getyearandmonth(n=0):
    '''
    get the year,month,days from today
    befor or after n months
    '''
    thisyear = int(year)
    thismon = int(mon)
    totalmon = thismon+n
    if(n>=0):
        if(totalmon<=12):
            days = str(get_days_of_month(thisyear,totalmon))
            totalmon = addzero(totalmon)
            return (year,totalmon,days)
        else:
            i = int(totalmon/12)
            j = int(totalmon%12)
            if(j==0):
                i-=1
                j=12
            thisyear += i
            days = str(get_days_of_month(thisyear,j))
            j = addzero(j)
            return (str(thisyear),str(j),days)
    else:
        if((totalmon>0) and (totalmon<12)):
            days = str(get_days_of_month(thisyear,totalmon))
            totalmon = addzero(totalmon)
            return (year,totalmon,days)
        else:
            i = int(totalmon/12)
            j = int(totalmon%12)
            if(j==0):
                i-=1
                j=12
            thisyear +=i
            days = str(get_days_of_month(thisyear,j))
            j = addzero(j)
            return (str(thisyear),str(j),days)

def addzero(n):
    '''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if(nabs<10):
        return "0"+str(nabs)
    else:
        return nabs

def get_today_month(n=0):
    '''
    获取当前日期前后N月的日期
    if n>0, 获取当前日期前N月的日期
    if n<0, 获取当前日期后N月的日期
    date format = "YYYY-MM-DD"
    '''
    (y,m,d) = getyearandmonth(n)
    arr=(y,m,d)
    if(int(day)<int(d)):
        arr = (y,m,day)
    return "-".join("%s" %i for i in arr)


def get_yesterday():
    '''
    获取昨天
    '''
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return str(yesterday)


if __name__=="__main__":
    print(todaystr())
    print(datetimestr())
    print(get_day_of_day(20))
    print(get_day_of_day(-3))
    print(get_today_month(-3))
    print(get_today_month(3))
    print(get_firstday_month(-2))
    print(get_lastday_month(-2))