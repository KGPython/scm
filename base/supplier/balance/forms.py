# -*- coding:utf-8 -*-
from django import forms

class BillInForm(forms.Form):
    shopid = forms.CharField(widget=forms.TextInput(attrs={"id":"shopCode","name":"shopCode","style":"width:200px","readonly":"readonly"}),max_length=1000,
                               required=False)
    start = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"start","name":"start",
                                                          "style":"width:200px"}),required=True,error_messages={"required":"起始日期不能为空",})
    end = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"end","name":"end",
                                                        "style":"width:200px"}),required=True,error_messages={"required":"截止日期不能为空",})
    sheetId  = forms.CharField(widget=forms.TextInput(attrs={"id":"sheetId","name":"sheetId","style":"width:200px"}),max_length=16,required=False)
    STATUS_CHOICES = (
        ('N', u'未确认'),
        ('Y', u'已确认'),
        ('', u'全部')
    )
    status = forms.ChoiceField(widget=forms.Select(attrs={"id":"status","name":"status"}),choices=STATUS_CHOICES,required=False)
    ORDER_CHOICES = (
        ('-editdate', u'制单日期'),
        ('sheetid', u'编码'),
        ('shopcode', u'结算位置'),
        ('-begindate', u'上次结算日期'),
        ('-enddate', u'本次结算日期'),
        ('flag', u'结算状态'),
        ('seenum', u'查看次数'),
    )
    orderStyle = forms.ChoiceField(widget=forms.Select(attrs={"id":"orderStyle","name":"orderStyle",}),choices=ORDER_CHOICES)