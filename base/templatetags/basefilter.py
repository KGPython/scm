#-*- coding:utf-8 -*-
__author__ = 'liubf'
from django import template
from django.template import Context
import datetime,time
from django.template.defaultfilters import date,stringfilter

register = template.Library()

@register.filter
def fillZero(value,n):
    f = ["0" for i in range(n)]
    s = "".join(f)

    return s+str(value)


@register.filter
def getPur(plist,key):
    flag = False
    for item in plist:
        if item[1]:
            for t in item[1]:
                if t["pcode"] == key:
                    flag = True
                    break;

    if flag:
        if key=="007":
            pur = "<a href='/scm/base/supp/repwd/' title='修改密码'>修改密码</a>"
        elif key == "277":
            pur = "<a href='/scm/base/balance/apply/edit/' style='color:red;'>您有未结算单据</a>"
    else:
        pur = "&nbsp;"
    t = template.Template(pur)
    c = Context()
    return t.render(c)

@register.filter
def cutNum(value):
   try:
        index = value.index(".")
        return value[index+1:]
   except:
       return value

#根据key读取字典value
@register.filter
def key(d,key_name):
    value = ""
    try:
        if isinstance(d,dict):
            value = d[str(key_name).strip()]
        else:
            value = d[key_name]
    except KeyError:
        value = ""
    return value

@register.filter
def isYes(value):
    if value:
        if str(value)=="1":
            return "是"
        else:
            return "否"
    else:
        return "否"

#比较是否过期:d1
@register.filter
def expired(d1,d2):
   rs = dtsub(d1,d2)
   if rs < 0:
       return "已过期"
   else:
       return "未过期"

#日期相减：d1 - d2的天数差
@register.filter
def dtsub(d1,d2):
    #datetime to string
    s1 = date(d1,"Y-m-d")
    s2 = date(d2,"Y-m-d")

    #string to date
    t1 = time.strptime(s1, "%Y-%m-%d")
    t2 = time.strptime(s2, "%Y-%m-%d")
    y1,m1,d1 = t1[0:3]
    y2,m2,d2 = t2[0:3]
    dt1 = datetime.datetime(y1,m1,d1)
    dt2 = datetime.datetime(y2,m2,d2)

    deff = dt1-dt2

    return deff.days

#去前后空格
@register.filter(is_safe=True)
@stringfilter
def trim(value):
    return value.strip()

#加法：v1 + v2
@register.filter
def add(v1,v2):
    return float(v1) + float(v2)

#减法：v1 - v2
@register.filter
def subtract(v1,v2):
    return float(v1) - float(v2)

#乘法：v1 * v2
@register.filter
def multiply(v1,v2):
    return float(v1) * float(v2)

#除法：v1 / v2
@register.filter
def divide(v1,v2):
    return float(v1) / float(v2)

 #取余：v1 % v2
@register.filter
def remainder(v1,v2):
    return float(v1) % float(v2)


from django.utils.safestring import mark_safe, SafeData
from django.utils.text import normalize_newlines
from django.utils.html import escape
@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def keep_spacing(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    value = mark_safe(value.replace('  ', ' &nbsp;'))
    return mark_safe(value.replace('\n', '<br />'))

@register.filter
def checkCode(d,key):
    str = "checked='checked'"
    for item in d:
        try:
            if key == item['orgcode']:
                return str
        except Exception as e:
            print(e)
    return ''

@register.filter
def checkTuple(tuple,key):
    str = "checked='checked'"
    for item in tuple:
        try:
            if key == item[0]:
                return str
        except Exception as e:
            print(e)
    return ''

@register.filter
def checkPayType(d,key):
    str = "checked='checked'"
    for item in d:
        try:
            if key == item['pid']:
                return str
        except Exception as e:
            print(e)
    return ''

@register.filter
def encodeStr(str):
    if str:
        return str.encode('latin-1').decode('gbk')
    else:
        return ""

@register.filter
def toInt(val):
    if val:
        return int(val)
    else:
        return ""

@register.filter
def isExist(val):
    print(val)
    return val