#-*- coding:utf-8 -*-
__author__ = 'liubf'
from django import forms
from base.models import Pubinfo

class retRoleForm(forms.Form):
    rcode = forms.CharField(max_length=20)
    nm = forms.CharField(required=True,max_length=50)
    CHIOCE_OPTION=(('1',u'有效'),('0',u'无效'))
    status = forms.ChoiceField(widget=(forms.Select()),choices=CHIOCE_OPTION)
    remark = forms.CharField(max_length=10)
    grpcode = forms.CharField(max_length=20)

class logForm(forms.Form):
    suppcode = forms.CharField(max_length=20,required=False)
    supname = forms.CharField(max_length=100,required=False)
    start = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"start","name":"start"}),required=True,error_messages={'required':'起始日期不能为空'})
    end = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"end","name":"end"}),required=True,error_messages={'required':'截止日期不能为空'})