#-*- coding:utf-8 -*-
__author__ = 'liubf'

import xlwt3 as xlwt
import os,decimal,datetime,time,random,hashlib
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from django.conf import settings
from base.utils import Constants
import configparser,json
import pymysql
import pymssql
import _mssql

from base.models import BasPur
def getSeeNum(request):
    urlCur = request.POST.get('urlCur','')
    res={}
    try:
        dataList = BasPur.objects.values('see_num').filter(bmoudule=urlCur)
        if len(dataList)>0:
            res=dataList[0]
            res['msg']='0'
        else:
            res['msg']='2'
    except Exception as e:
        print(e)
        res['msg']='1'

    return HttpResponse(json.dumps(res))

def setSeeNum(request):
    urlCur = request.POST.get('urlCur','')
    seeNum = request.POST.get('seeNum','')
    seeNum = str(int(seeNum)+1)
    res={}
    try:
        BasPur.objects.filter(bmoudule=urlCur).update(see_num=seeNum)
        # conn = getMysqlConn()
        # cur = conn.cursor()
        #
        # sql = 'update bas_pur set see_num = see_num+1 where bmoudule = "'+urlCur+'"'
        # cur.execute(sql)
        # conn.commit()
        res['msg']='0'
    except Exception as e:
        print(e)
        res['msg']='1'

    return HttpResponse(json.dumps(res))

def convertToStr(val,*arg):
    if arg:
        fmt,divisor = arg[0],arg[1]
    else:
        fmt,divisor = None,None

    if not fmt:
        fmt = "0.00"
    if not divisor:
        divisor = 10000

    if isinstance(val,decimal.Decimal):
        return str(float((val/divisor).quantize(decimal.Decimal(str(fmt)))))
    else:
        if val:
            return str(float(val))
        else:
            return "0.00"

def quantize(val,*arg):
    if arg:
        fmt,divisor = arg[0],arg[1]
    else:
        fmt,divisor = None,None

    if not fmt:
        fmt = "0.00"
    if not divisor:
        divisor = 10000

    if isinstance(val,decimal.Decimal):
        return (val/divisor).quantize(decimal.Decimal(str(fmt)))
    else:
        if val:
            return val
        else:
            return decimal.Decimal("0.00")

def encodeStr(str):
    if str:
        return str.encode('latin-1').decode('gbk')
    else:
        return ""
def getProperties(module,key):
    """根据key读取配置文件value"""
    try:
        config = configparser.ConfigParser()
        #linux
        file = "{base_root}/ConfigParser.conf".format(base_root=Constants.BASE_ROOT)
        config.read(file)
        #windows
        # config.read("ConfigParser.conf")
        val = config.get(module,key)
    except Exception as e:
        val = ""
        print(e)
    return val

#获取mysql数据库连接
def getMssqlConn(as_dict=True):
    conn = pymssql.connect(host=Constants.SCM_DB_SERVER,
                           port=Constants.SCM_DB_PORT,
                           user=Constants.SCM_DB_USER,
                           password=Constants.SCM_DB_PASSWORD,
                           database=Constants.SCM_DB_DATABASE,
                           charset='utf8',
                           as_dict=as_dict)
    return conn

def get_MssqlConn():
    conn = _mssql.connect(server=Constants.SCM_DB_SERVER,
                           port=Constants.SCM_DB_PORT,
                           user=Constants.SCM_DB_USER,
                           password=Constants.SCM_DB_PASSWORD,
                           database=Constants.SCM_DB_DATABASE,
                           charset='utf8')
    return conn

#获取mysql数据库连接
def getMysqlConn():
    conn = pymysql.connect(host=Constants.SCM_DB_MYSQL_SERVER,
                           port=Constants.SCM_DB_MYSQL_PORT,
                           user=Constants.SCM_DB_MYSQL_USER,
                           password=Constants.SCM_DB_MYSQL_PASSWORD,
                           db=Constants.SCM_DB_MYSQL_DATABASE,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    return conn

#关闭连接
def close(conn,cur):
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
    except Exception as e:
        print(e)

def getDBVal(row,key):

    return row[key].encode('latin-1').decode('gbk')


#md5
def md5(str):

    md5 = hashlib.md5()
    if str:
        md5.update(str.encode(encoding='utf-8'))

    return md5.hexdigest()

#日期相减：d1 - d2的天数差
def dtsub(d1,d2):
    #datetime to string
    s1 = d1.strftime('%Y-%m-%d')
    s2 = d2.strftime('%Y-%m-%d')

    #string to date
    t1 = time.strptime(s1, "%Y-%m-%d")
    t2 = time.strptime(s2, "%Y-%m-%d")
    y1,m1,d1 = t1[0:3]
    y2,m2,d2 = t2[0:3]
    dt1 = datetime.datetime(y1,m1,d1)
    dt2 = datetime.datetime(y2,m2,d2)

    deff = dt1-dt2

    return deff.days
#获取request对象中值，为空时返回默认值
def getReqVal(request,key,default=None):

    if request.method=="GET":
        val = request.GET.get(key,default)
    elif request.method=="POST":
        val = request.POST.get(key,default)

    return val

def getReqList(request,key,default=None):

    if request.method=="GET":
        val = request.GET.getlist(key,default)
    elif request.method=="POST":
        val = request.POST.getlist(key,default)

    return val

def getResponse(response,type,fname):
    response['Content-Type']=type
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    response['Pragma'] = "no-cache"
    response['Expires'] = "0"
    return response

#excel到出
#@param title sheet名称 非必填
#@param titles 表格标题 [("名称","列宽","key")] 必填
#@param list 表格数据 [("value","value"),("value","value"),...] or [["val","val"],...] or [{"key":value,"key":value},{},...]
#@param slist 合计["","","","",sum1,sum2,sum3]
#@param dictlist code 转 name 字典 [{"key":value,"key":value},{},...]
#@param fmtlist 数据格式化列表["","","","","0.00","0.00","0.0"]
def exportXls(sheetname,titles,datalist,sumlist,dictlist,fmtlist):
    #3.写入excel
    if not sheetname:
        sheetname = "Sheet1"

    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet(sheetname,cell_overwrite_ok=True)

    #添加title
    insertTitle(sheet,titles)

    #添加cell
    count = insertCell(sheet,datalist,titles,dictlist,fmtlist)

    #添加合计
    if sumlist:
        insertSum(sheet,count,sumlist,fmtlist)

    return book

def insertTitle2(sheet,titles,keyList,widthList):
     #设置导出文件标题样式
    tstyle = xlwt.easyxf('pattern: pattern solid, fore_colour blue_gray; font: bold on,name SimSun,height 230,'
                         'colour_index 1;borders: left thin,top thin,right thin,bottom thin;align: horiz center,vert center')

    #设置行高
    sheet.row(0).height_mismatch = True
    sheet.row(0).height =500
    #设置列宽
    if widthList:
        for i in range(len(widthList)):
            sheet.col(i).width = 0x0d00 + widthList[i]

    for i in range(len(titles)):
        trow = titles[i]

        if keyList:
            for j in range(len(keyList)):
               sheet.write(i,j,"",tstyle)

        for col in trow:
            #写入导出文件标题
            sheet.write_merge(i,i+col[2]-1,col[1],col[1]+col[3]-1,str(col[0]),tstyle)

#添加合计
def insertSum2(sheet,keylist,count,sdict,index):
    tstyle = xlwt.easyxf('pattern: pattern solid, fore_colour blue_gray; font: bold on,name SimSun,height 200,'
                         'colour_index 1;borders: left thin,top thin,right thin,bottom thin;align: horiz center,vert center')
    sstyle = xlwt.easyxf('pattern: pattern solid,fore_colour white;font:name SimSun,height 200;'
                         'borders:left thin,top thin,right thin,bottom thin;align: horiz center,vert center')

    slist=sorted(sdict.keys(), key=lambda d:d)
    for key in slist:
        item = sdict[key]
        #写入合计文本
        colindex = index
        col1 = item[keylist[0]]
        sheet.write_merge(count,count,0,colindex-1,col1,tstyle)
        #写入合计数值
        for j in range(1,len(keylist)):
            k = keylist[j]
            if k in item:
                val = item[k]
                sheet.write(count,j,val,sstyle)
            else:
                sheet.write(count,j,'',sstyle)
        count += 1
    return count

def insertCell2(sheet,count,datalist,keylist,dictlist):
    #设置商品不存在时提示信息的样式
    sstyle = xlwt.easyxf('pattern: pattern solid,fore_colour white;font:name SimSun,height 200;'
                         'borders:left thin,top thin,right thin,bottom thin;align: horiz center,vert center')
    #根据商品条码查询商品信息
    for i in range(0,len(datalist)):
        row = datalist[i]
        #数据为list、tuple
        if isinstance(row,list) or isinstance(row,tuple):
            for j in range(len(row)):
                cell = row[j]
                dt = None
                if dictlist:
                    dt = dictlist[j]
                if dt:
                     #根据key取value
                    sheet.write(count,j,dt[str(cell)],sstyle)
                else:
                    sheet.write(count,j,cell,sstyle)
        elif isinstance(row,dict):
           #数据为字典
           for j in range(len(keylist)):
                dt = None
                if dictlist:
                    dt = dictlist[j]
                key = keylist[j]
                cell = row.get(key)
                if isinstance(cell,str):
                    cell = cell.strip()
                if dt:
                     #根据key取value
                    sheet.write(count,j,dt[str(cell)],sstyle)
                else:
                    sheet.write(count,j,cell,sstyle)
        count += 1
#        sheet.row(i).hidden=1    隐藏行
    return count

#添加标题
def insertTitle(sheet,titles):
     #设置导出文件标题样式
    styleTitle = xlwt.XFStyle()

    #设置背景色
    bgcolor = xlwt.Pattern
    bgcolor.pattern = bgcolor.SOLID_PATTERN
    #
    bgcolor.pattern_fore_colour = 19
    bgcolor.pattern_back_colour = 19
    styleTitle.pattern = bgcolor

    #设置字体
    fontTitle = xlwt.Font()
    fontTitle.name = 'SimSun'    # 指定“宋体”
    fontTitle.colour_index=1
    fontTitle.bold=True
    fontTitle.height=300
    styleTitle.font = fontTitle

    #设置行高
    sheet.row(0).height_mismatch = True
    sheet.row(0).height =500

    for i in range(len(titles)):
        trow = titles[i]
        #写入导出文件标题
        sheet.write(0,i,str(trow[0]),styleTitle)
        #设置列宽
        sheet.col(i).width = 0x0d00 + int(trow[1])

#添加数据
def insertCell(sheet,datalist,titles,dictlist,fmtlist):
     #设置商品不存在时提示信息的样式
    styleExcept = xlwt.XFStyle()
    fontExcept = xlwt.Font()
    fontExcept.name = 'SimSun'    # 指定“宋体”
    fontExcept.colour_index=2
    fontExcept.bold=True
    # styleExcept.borders=borders
    styleExcept.font = fontExcept

    #根据商品条码查询商品信息
    count = 0
    for i in range(0,len(datalist)):
        count += 1
        row = datalist[i]
        #数据为list、tuple
        if isinstance(row,list) or isinstance(row,tuple):
            for j in range(len(row)):
                cell = row[j]
                fmt,dt = None,None
                if fmtlist:
                    fmt = fmtlist[j]
                if dictlist:
                    dt = dictlist[j]

                if isinstance(cell,decimal.Decimal) and fmt:
                    sheet.write(i+1,j,cell.quantize(decimal.Decimal(str(fmt))))
                else:
                    if dt:
                         #根据key取value
                        sheet.write(i+1,j,dt[str(cell)])
                    else:
                        if isinstance(cell,datetime.datetime) and fmt:
                            sheet.write(i+1,j,cell.strftime(fmt))
                        else:
                            sheet.write(i+1,j,cell)
        elif isinstance(row,dict):
           #数据为字典
           for j in range(len(titles)):

                fmt,dt = None,None
                if fmtlist:
                    fmt = fmtlist[j]
                if dictlist:
                    dt = dictlist[j]

                key = titles[j]

                cell = row.get(key[2])
                if isinstance(cell,decimal.Decimal) and fmt:
                    sheet.write(i+1,j,str(cell.quantize(decimal.Decimal(str(fmt)))))
                else:
                    if dt:
                         #根据key取value
                        sheet.write(i+1,j,dt[str(cell)])
                    else:
                        if isinstance(cell,datetime.datetime) and fmt:
                            sheet.write(i+1,j,cell.strftime(fmt))
                        else:
                            sheet.write(i+1,j,cell)
    return count

#添加合计
def insertSum(sheet,count,slist,fmtlist):
    styleFooter = xlwt.XFStyle()
    #设置字体
    footerFont = xlwt.Font()
    footerFont.name = 'SimSun'    # 指定“宋体”
    footerFont.colour_index=0
    footerFont.bold=True
    footerFont.height=230
    styleFooter.font = footerFont

    count += 1
    for i in range(len(slist)):
        sum = slist[i]
        fmt = fmtlist[i]
        if isinstance(sum,decimal.Decimal) and fmt:
             sheet.write(count,i,sum.quantize(decimal.Decimal(fmt)),styleFooter)
        else:
            sheet.write(count,i,sum,styleFooter)

#生成验证码
def   verifycode(request,key):
    # 随机颜色1:
    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    root = settings.BASE_DIR+Constants.FONT_ARIAL
    font = ImageFont.truetype(root, 50)     #36 - 字体大小，数值大字体大
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())

    # 输出文字:
    chars=['0','1','2','3','4','5','6','7','8','9',
           #'a','b','c','d','e','f','g','h','i','j','k','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           #'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
           ]
    y = [y for y in [random.randint(x-x, len(chars)-1) for x in range(4)] ]
    charlist = [chars[i] for i in y]

    rcode = ''.join(map(str,charlist))

    for t in range(len(charlist)):
        draw.text((60 * t + 10, 10), charlist[t], font=font, fill=rndColor2())

    # 模糊:
    #image = image.filter(ImageFilter.BLUR)

    #将图片保存到本地磁盘
    #image.save('code.jpg', 'jpeg')

    #将验证码转换成小写的，并保存到session中
    request.session[key] =rcode

    return image

def rmbupper(arg):
    """
    人名币小写转大写，整数部分处理到万亿,小数部分只处理2位
    """
    map  = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
    unit = ["分","角","元","拾","佰","仟","万","拾","佰","仟","亿",
            "拾","佰","仟","万","拾","佰","仟","兆"]
    nums = []   #取出每一位数字，整数用字符方式转换避大数出现误差
    if type(arg) is float:
        for i in range(len(unit)-3, -3, -1):
            if arg >= 10**i or i < 1:
                nums.append(int(str(arg/(10**i)).split('.')[0])%10)
    else:
        nums = [int(i) for i in str(arg)+'00']

    words = []
    zflag = 0   #标记连续0次数，以删除万字，或适时插入零字
    start = len(nums)-3
    for i in range(start, -3, -1):   #使i对应实际位数，负数为角分
        if 0 != nums[start-i] or len(words) == 0:
            if zflag:
                words.append(map[0])
                zflag = 0
            words.append(map[nums[start-i]])
            words.append(unit[i+2])
        elif 0 == i or (0 == i%4 and zflag < 3): #控制‘万/元’
            words.append(unit[i+2])
            zflag = 0
        else:
            zflag += 1

    if words[-1] != unit[0]:    #结尾非‘分’补整字
        words.append("整")
    return ''.join(words)

class PinYin(object):
    def __init__(self, dict_file=Constants.WORD_DATA):

        self.word_dict = {}
        self.dict_file = settings.BASE_DIR+dict_file
        self.load_word()


    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with open(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]


    def hanzi2pinyin(self, string=""):
        result = []
        for char in string:
            key = '%X' % ord(char)
            value = self.word_dict.get(key, char).split()[0][:-1].lower()
            if value:
                result.append(value)
            else:
               result.append(char)

        return result


    def hanzi2pinyin_split(self, string="", split=""):
        result = self.hanzi2pinyin(string=string)
        return split.join(result)

def insertSysLog(conn,loginid,workstattionid,moduleid,eventid,note):
    """保存操作日志"""
    sql = """insert into SysLog(LoginID,WorkstationID,ModuleID,EventID,Note)
             values({LoginID},{WorkstationID},{ModuleID},{EventID},'{Note}')
             """.format(Note=note,LoginID=loginid,WorkstationID=workstattionid,ModuleID=moduleid,EventID=eventid)
    conn.execute_non_query(sql)

def getCurrentMonthDay(currentday):
    currentMonth = currentday.strftime('%m')
    currentYear = currentday.strftime('%Y')
    d1 = datetime.datetime(int(currentYear),int(currentMonth),1)
    d2 = datetime.datetime(int(currentYear),int(currentMonth)+1,1)
    days = d2 - d1
    day = days.days
    return datetime.date(int(currentYear),int(currentMonth),1),\
           datetime.date(int(currentYear),int(currentMonth),day),day

def testmssql():
    conn = getMssqlConn()
    cur = conn.cursor()
    sql = "select top 10 [ID],[Name] from [Shop]"
    cur.execute(sql)
    list = cur.fetchall()
    for row in list:
        print(row["ID"],getDBVal(row,"Name"))

    # sql = "insert into CustReceiveItem0 values( 'CM01201601120002','203','测试保存2','211','2016-01-12 16:53:37','0','212','10','204','205','209','207','213')"
    # cur.execute(sql)
    # conn.commit()
    conn.close()

###
# 排名函数
# lis：需要排序的list
# key：排序的参照对象
# name:名次存放的字段名称
###
def ranking(lis,key,name):
    lis.sort(key=lambda x:x[key])
    j = 1
    for i in range(0,len(lis)):
        if i > 0:
            a = lis[i-1]
            b = lis[i]
            if float(a[key]) != float(b[key]):
                j += 1
            b[name]= j
            a[key] = str(a[key])+'%'
        else:
            a = lis[i]
            a[name]= j
    return lis



if __name__ == "__main__":
    print(">>>__main__")
    # d1 = datetime.datetime.now()
    # d2 = datetime.datetime.strptime("2015-12-10",'%Y-%m-%d')
    # print(dtsub(d1,d2))
    # testmssql()
    # d = (datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=1).strftime("%Y%m")
    # print(datetime.timedelta(1))
    # print(getDBVal({"Name":"we"},"Name"))

    # print((datetime.date.today().replace(day=1) - datetime.timedelta(1)).replace(day=1))
    # print(datetime.date.today().replace(day=1))
    # print(datetime.timedelta(1))
    # print(datetime.date.today().replace(day=1) - datetime.timedelta(1))
    #
    # s = b"\xe5\x8f\x96\xe5\xae\xa1\xe6\xa0\xb8\xe5\x91\x98\xe7\x9a\x84\xe8\x8b\xb1\xe6\x96\x87\xe5\x90\x8d\xe5\x87\xba\xe9\x94\x99\xef\xbc\x8c\xe8\xaf\xb7\xe6\xa0\xb8\xe5\xae\x9e"
    # print(str(s,"utf-8"))
    # print(getCurrentMonthDay(datetime.date.today()))
    print(getProperties("bill","scm.bill.islimit"))