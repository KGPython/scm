# -*- coding:utf-8 -*-
from django import forms

class BillInForm(forms.Form):
    shopid = forms.CharField(widget=forms.TextInput(attrs={"id":"shopCode","name":"shopCode","readonly":"readonly"}),max_length=1000,
                               required=False)
    start = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"start","name":"start"}),required=True,error_messages={"required":"起始日期不能为空",})
    end = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"end","name":"end"}),required=True,error_messages={"required":"截止日期不能为空",})
    sheetId  = forms.CharField(widget=forms.TextInput(attrs={"id":"sheetId","name":"sheetId"}),max_length=16,required=False)
    STATUS_CHOICES = (
        ('N', u'未确认'),
        ('Y', u'已确认'),
        ('', u'全部')
    )
    status = forms.ChoiceField(widget=forms.Select(attrs={"id":"status","name":"status"}),choices=STATUS_CHOICES,required=False)

    FLAG_CHOICES = (
        ('', u'全部'),
        ('0', u'1-制单未审核 '),
        ('1,4', u'2-单据待审批'),
        ('2', u'3-扣项缴款待审核'),
        ('3', u'4-付款待审核'),
        ('100', u'5-已付款')
    )
    flag = forms.ChoiceField(widget=forms.Select(attrs={"id":"status","name":"status"}),choices=FLAG_CHOICES,required=False)
    ORDER_CHOICES = (
        ('shopid', u'结算位置'),
        ('sheetid', u'供应商编码'),
        ('-begindate', u'上次结算日期'),
        ('-enddate', u'本次结算日期'),
        ('-editdate', u'制单日期'),
        ('flag', u'审核状态'),
        #('seenum', u'查看次数'),
    )
    orderStyle = forms.ChoiceField(widget=forms.Select(attrs={"id":"orderStyle","name":"orderStyle",}),choices=ORDER_CHOICES)