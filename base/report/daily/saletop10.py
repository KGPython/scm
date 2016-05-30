# -*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from base.utils import MethodUtil

@csrf_exempt
def index(request):
    pass