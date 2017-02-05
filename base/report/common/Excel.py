from django.http import StreamingHttpResponse
import os
from base.utils import Constants
def saveToExcel(name,wb):
    FILE_ROOT =  Constants.REPORT_EXCEL
    file_full_path = os.path.join(FILE_ROOT, name)
    stu = wb.save(file_full_path)
    return stu

def downloadReportExcel(request):
    fname = request.GET.get('fname')

    FILE_ROOT = Constants.REPORT_EXCEL
    the_file_name = os.path.join(FILE_ROOT,fname)
    response = StreamingHttpResponse(readFile(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fname)
    response['Pragma'] = "no-cache"
    response['Expires'] = "0"
    return response


#读取文件
def readFile(filePath, buf_size=262144):
    #存放文件路径
    f = open(filePath,"rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()

def isExist(fname):
    flag = True
    FILE_ROOT = Constants.REPORT_EXCEL
    file_full_path = os.path.join(FILE_ROOT,fname)
    if not os.path.exists(file_full_path):
        flag = False
    return flag