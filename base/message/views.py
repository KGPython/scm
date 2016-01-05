#-*- coding:utf-8 -*-
import random
__author__ = 'liubf'

from django.db.models import Q
from base.models import Pubinfo,BasStub
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponseRedirect
import base.utils.Constants as constants
import os
from .forms import *
import time,datetime
import sys
from django.core.paginator import Paginator,Page

#读取文件
def readFile(fn, buf_size=262144):
    rootPath = os.getcwd()

    #存放文件路径
    path = rootPath
    file = path+fn
    f = open(file,"rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()

#下载附件
def download(request):
    file = request.GET.get("filename","")
    filename = file.split("/")

    response = StreamingHttpResponse(readFile(file))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename[len(filename)-1])
    response['Pragma'] = "no-cache"
    response['Expires'] = "0"
    return response

def info(request):
    infocode = str(request.GET.get("infocode"))
    if infocode:
        pub = Pubinfo.objects.values("infocode","infotype","checker","subtime","content","title","depart","grpcode","accesstype","status","username","usergrpcode","usergrpname","departname","mailpath").get(Q(infocode=infocode))
    else:
        pub = Pubinfo()
    return render(request,"notice_article.html",{"pub":pub,"infoTypeName":constants.PUBINFO_TYPE[pub['infotype']]})

#根据条件查询协同信息
def findPubInfoAllByCon(user):

    #accesstype 接收方类型：11-指定编码(多个用逗号隔开)，13-全部
    #infotype
    utype = user["utype"]
    #供应商查询已接收通知
    if utype=="2":
        result = Pubinfo.objects.filter(Q(infotype=0) & ((Q(accesstype=11) & Q(depart=user["grpcode"])) | (Q(accesstype=13) & Q(depart=""))))\
            .order_by("-infocode")\
            .values("infocode","infotype","checker","subtime","content","title","depart","grpcode","accesstype","status","username","usergrpcode","usergrpname","departname","mailpath")

    else:
        #零售商查询已发送出通知
        result = Pubinfo.objects.filter(Q(checker=user["ucode"]))\
            .order_by("-infocode")\
            .values("infocode","infotype","checker","subtime","content","title","depart","grpcode","accesstype","status","username","usergrpcode","usergrpname","departname","mailpath")

    return result

def findPubInfoTotalCount(user):
    total = Pubinfo.objects.filter(Q(infotype=1) & Q(usergrpcode=user.grpcode) & (Q(accesstype=11) & Q(depart=user.ucode) | Q(accesstype=13)))\
            .count()
    return total

def msglist(request):
    #获取seesion信息
    grpCode = request.session.get('s_grpcode','')#000069
    userCode = request.session.get('s_ucode')
    userType = request.session.get('s_utype')
    if userType=="2":
        userGrpCode = request.session.get('s_suppcode')
    elif userType=="1":
        userGrpCode = grpCode

    page = request.GET.get('page',1)
    infoList=[]
    infoCode = ''
    start = ''
    end = ''
    if request.method == 'POST':
        flag = request.POST.get('flag','')
        form=msgForm(request.POST)
        if form.is_valid():
            infoCode = form.cleaned_data['infocode']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']

            #基础查询条件初始化
            q = Q()
            kwargs = {}
            if infoCode:
                kwargs.setdefault('infocode__contains',infoCode)
            kwargs.setdefault('subtime__gte',start.strftime("%Y-%m-%d")+" 00:00:00")
            kwargs.setdefault('subtime__lte',end.strftime("%Y-%m-%d")+" 23:59:59")
            kwargs.setdefault('grpcode',grpCode)

            if flag == 'msgIn':
                # 根据用户类型，获特殊查询条件
                if userType == "2":
                    q.add((Q(depart=userGrpCode) & Q(accesstype='11')) | (Q(accesstype='13') & Q(depart='')),Q.AND)
                else:
                    q.add(((Q(depart=userCode) & Q(accesstype='21')) | (Q(accesstype='23') & Q(depart=''))),Q.AND)

                #获取数据列表
                infoList = Pubinfo.objects.values("infocode","title","depart","subtime","usergrpname","username","content","checker")\
                                          .filter(q,**kwargs)
            if flag == 'msgOut':
                q.add(Q(checker=userCode),Q.AND)
                infoList = Pubinfo.objects.values("infocode","title","depart","subtime","usergrpname","username","content","checker")\
                                          .filter(q,**kwargs)
    else:
        infoCode = request.GET.get('infocode','')
        start = request.GET.get('start','')
        if not start:
            start = (datetime.date.today().replace(day=1)).strftime("%Y-%m-%d")

        end = request.GET.get('end','')
        if not end:
            end = datetime.datetime.today().strftime("%Y-%m-%d")

        flag = request.GET.get('flag','')
        data = {'infocode':infoCode,'start':start,'end':end,'flag':flag}
        form=msgForm(data)
        if request.GET.get('action') == 'del':    #“删除”操作
            try:
                infoObj=Pubinfo.objects.get(infocode=infoCode)
            except:
                infoObj=None
            if infoObj:
                mailPath = infoObj.mailpath
                rootPath = os.getcwd()  #获取工程目录
                if os.path.isfile(rootPath+mailPath):
                    os.remove(rootPath+mailPath)
                infoObj.delete()
            return HttpResponseRedirect('/scm/base/msg/msglist/?start='+start+'&end='+end+'&flag='+flag)

        #基础查询条件初始化
        q = Q()
        kwargs = {}
        kwargs.setdefault('subtime__gte',start+" 00:00:00")
        kwargs.setdefault('subtime__lte',end+" 23:59:59")

        if flag == 'msgIn':
            # 根据用户类型，获特殊查询条件
            if userType == "2":
                q.add((Q(depart=userGrpCode) & Q(accesstype='11')) | (Q(accesstype='13') & Q(depart='')),Q.AND)
            else:
                q.add(((Q(depart=userCode) & Q(accesstype='11')) | (Q(accesstype='13') & Q(depart=''))),Q.AND)

            #获取数据列表
            infoList = Pubinfo.objects.values("infocode","title","depart","subtime","usergrpname","username","content","checker")\
                                          .filter(q,**kwargs)

        if flag == 'msgOut':
            q.add(Q(checker=userCode),Q.AND)
            infoList = Pubinfo.objects.values("infocode","title","depart","subtime","usergrpname","username","content","checker")\
                                          .filter(q,**kwargs)

    paginator=Paginator(infoList,20)
    try:
        rslist=paginator.page(page)
    except Exception as e:
        print(e)
        rslist = Page()
    return render(request,
                  'user_notice.html',
                  {
                      "form":form,
                      "userType" : userType,
                      "userGrpCode" : userGrpCode,
                      "userCode" : userCode,
                      "infoList":rslist,
                      "start":str(start),
                      "end":str(end),
                      "infoCode":infoCode,
                      "flag":flag,
                      "page":page
                  })


timestr = time.strftime("%Y-%m-%d %H:%M:%S")

def msgPreview(request):
    infoCode = request.GET.get("infocode","")
    infoObj = Pubinfo.objects.values("title","content","checker","subtime","mailpath").get(infocode=infoCode)
    return render(request,'notice_preview.html',locals())

def msgCreate(request):

    #session传递参数
    grpCode = request.session.get('s_grpcode','')#00069

    userCode = request.session.get('s_ucode')
    userName = request.session.get('s_uname')
    userType = request.session.get('s_utype')

    if userType=="2":
        userGrpName = request.session.get('s_suppname','')
        userGrpCode = request.session.get('s_suppcode')
    elif userType=="1":
        userGrpName = request.session.get('s_grpname','')
        userGrpCode = grpCode

    if request.method == 'GET':
        #地址栏传递参数
        action = request.GET.get("action")
        infoType = request.GET.get('infotype','')
        infoCode = request.GET.get('infocode','')
        #查询
        if infoCode:
            info = Pubinfo.objects.values("checker","title","content","username","subtime","mailpath","depart").get(infocode=infoCode)
            #获取附件名称
            mailpath = info.get('mailpath','')
            if mailpath:
                filename = mailpath.split('/')
                filename = filename[len(filename)-1]
    if request.method == 'POST':
        action = request.POST.get("action")
        infoCode = request.POST.get('infocode','')
        accessType = request.POST.get('accesstype')
        infoType = request.POST.get('infotype')
        title = request.POST.get('title','').strip()
        content = request.POST.get('content','').strip()
        depart = request.POST.get('depart','').strip()
        fileObj= request.FILES.get('file')
        oldpath = request.POST.get('oldpath')

        mailpath=''
        rootPath = os.getcwd()  #获取工程目录
        if oldpath:
            os.remove(rootPath+oldpath)
        if fileObj:
            mailpath=uploadFile(fileObj)

        #编辑
        if infoCode and action!="answer":
            Pubinfo.objects.filter(infocode=infoCode).update(title=title,content=content,depart=depart,mailpath=mailpath,subtime=timestr)
            succ = "1" #设置提交成功返回信息，在前端展现
        #创建
        else:
            info = Pubinfo()
            #session中user信息
            info.checker = userCode
            info.grpcode = grpCode
            info.username = userName
            info.usergrpcode = userGrpCode
            info.usergrpname = userGrpName

            #表单提交信息
            info.infotype = infoType
            info.accesstype = accessType
            info.depart = depart
            info.title = title
            info.content = content
            info.mailpath = mailpath
            info.subtime = timestr

            infoCode = getInfoCode(request,'pubinfoid')
            info.infocode= infoCode

            info.save()
            if action=="answer":
                succ = "3"
            else:
                succ = "2" #设置提交成功返回信息，在前端展现
    return render(request, 'noticeCreate.html',locals())

def uploadFile(fileObj):
    rootPath = os.getcwd()  #获取工程目录
    UPLOAD_ROOT = rootPath+'/upload/message/'
    if not os.path.exists(UPLOAD_ROOT):
        os.makedirs(UPLOAD_ROOT)

    microsecond = datetime.datetime.now().microsecond
    file_name = fileObj.name #附件存储名称
    file_name_list = file_name.split(".")
    file_name = str(microsecond)+"."+file_name_list[1]     #上传附件的存储名称

    file_full_path = os.path.join(UPLOAD_ROOT, file_name)

    dest = open(file_full_path,'wb+')
    dest.write(fileObj.read())
    dest.close()
    filePath = '/upload/message/'+file_name
    return filePath

#生成infocode
def getInfoCode(request,id):
    infoCode = ''
    itemId = id
    stub = BasStub.objects.get(itemid=itemId)

    lastNum = int(stub.lastnum)+1
    lastNum = str(lastNum)
    numlen = stub.numlen

    strNum =''
    for i in range(len(lastNum),numlen):
        strNum += '0'
    infoCode = strNum + lastNum

    stub.lastnum = lastNum
    stub.save()
    return infoCode
