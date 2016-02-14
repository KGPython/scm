# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from django import forms

class retOrderForm(forms.Form):
    status = forms.ChoiceField(widget=forms.Select(),choices=(('','全部'),('N',u'未确认'),('Y',u'已确认')),required=False)
    state = forms.ChoiceField(widget=forms.Select(),choices=(('','全部'),('N',u'未过期'),('Y',u'已过期')),required=False)
    spercode = forms.CharField(max_length=20,required=False)
    ordercode = forms.CharField(max_length=20,required=False)
    start = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"start","name":"start"}),required=True,error_messages={"required":"截止日期不能为空",})
    end = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"end","name":"end"}),required=True,error_messages={"required":"截止日期不能为空",})
    shopcode = forms.CharField(widget=forms.TextInput(attrs={"id":"shopCode","name":"shopCode"}),required=False)
    ORDER_LIST=(('spercode',u'供应商编码'),('checkdate',u'审核日期'),('ordercode',u'订单编号'),('shopcode',u'交货门店'))
    orderstyle = forms.ChoiceField(widget=forms.Select(),choices=ORDER_LIST,required=False)