#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.conf import settings
from re import compile
from django.http import HttpResponseRedirect as redirect
from django.shortcuts import render

EXEMPT_URLS=[compile(settings.LOGIN_URL.lstrip('/'))]

if hasattr(settings,'LOGIN_EXEMPT_URLS'):
	EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginMiddleware(object):

    def process_request(self, request):
        #此用户没有登陆，判断请求的路径是否合法：
        path = request.path_info.lstrip('/')
        #不过滤css/js/image
        if path.find("css/")==-1 and path.find("js/")==-1 and path.find("image/")==-1:
            #如果用户未登录，跳转到登录页面
            if 's_user' not in request.session or not request.session.get("s_user",default=None):
                    if not any(m.match(path) for m in EXEMPT_URLS):
                        print(">>>>>>>>>用户未登录，地址不合法："+path)
                        return redirect(settings.LOGIN_URL)
                    else:
                        print(">>>>>>>>>无限制地址："+path)
            else:
                s_ucode =  request.session.get("s_ucode",default=None)
                print(">>>>>>>>>登录用户："+s_ucode,path)
        else:
            print(">>>>>>>>>static文件地址，不过滤："+path)
