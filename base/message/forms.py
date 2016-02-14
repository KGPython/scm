#-*- coding:utf-8 -*-
__author__ = 'liubf'
from django import forms
from base.models import Pubinfo

class PubInfoForm(forms.Form):
    usergrpcode = forms.CharField(max_length=20)
    infotype = forms.CharField(max_length=4)

    class Meta:
        model = Pubinfo
        fields = ['infocode', 'infotype', 'checker', 'subtime',
                  'content', 'title', 'depart',  'grpcode',
                  'accesstype', 'status','username','usergrpcode',
                  'usergrpname','departname','mailpath']
class msgForm(forms.Form):
    infocode = forms.CharField(widget=forms.TextInput(attrs={"name":"infocode"}),max_length=20,required=False)
    start = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"start","name":"start"}),required=True,error_messages={"required":"起始日期不能为空",})
    end = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"end","name":"end"}),required=True,error_messages={"required":"截止日期不能为空",})
