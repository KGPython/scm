#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from base.utils import Constants as cts
from base.models import EstimateYear
import datetime;
import xlrd,os

@csrf_exempt
def impt(request):
    fileObj = request.FILES.get('file')
    status = "failure"
    today = datetime.date.today()
    try:
        if fileObj:
            #1.上传文件
            file_path = uploadFile(fileObj)
            #2.读取内容
            book = xlrd.open_workbook(file_path)

            sheet = book.sheet_by_index(0)
            sheet1 = book.sheet_by_index(1)
            nrows = sheet.nrows  # 行总数
            ncols = sheet.ncols  # 列总数

            for i in range(1,nrows):
                shopid = sheet.cell(i, 0).value
                for j in range(2,ncols):
                    salevalue = sheet.cell(i,j).value
                    salegain = sheet1.cell(i,j).value
                    dateid = datetime.date(year=today.year,month=j-1,day=1).strftime("%Y-%m-%d")
                    # 3.写入数据库
                    try:
                        #已存在则删除
                        est = EstimateYear.objects.get(shopid=shopid,dateid=dateid)
                        est.delete()
                    except:
                        pass

                    ey = EstimateYear()
                    ey.shopid=shopid
                    ey.dateid=dateid
                    ey.salevalue=salevalue
                    ey.salegain=salegain
                    ey.createtime=datetime.datetime.today()
                    ey.save()
            status = "success"
    except Exception as e:
        print(e)

    return render(request, "admin/retail_estimate.html",{"status":status})

def uploadFile(fileObj):
    UPLOAD_ROOT = cts.BASE_ROOT+'/upload/temp/'

    file_name = fileObj.name
    file_full_path = os.path.join(UPLOAD_ROOT, file_name)
    if os.path.exists(file_full_path):
        os.remove(file_full_path)

    dest = open(file_full_path,'wb+')
    dest.write(fileObj.read())
    dest.close()

    return file_full_path