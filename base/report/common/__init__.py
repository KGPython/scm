# -*-  coding:utf-8 -*-
from django.shortcuts import render


def index(request):
    if request.method == 'POST':
        pass
    return render(request, '', locals())