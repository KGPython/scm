#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index():
    pass

@csrf_exempt
def query():
    pass

@csrf_exempt
def download():
    pass