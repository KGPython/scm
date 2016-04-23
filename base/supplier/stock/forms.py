# -*- coding:utf-8 -*-
from django import forms


class StockForm(forms.Form):
    shopCode = forms.CharField(widget=forms.TextInput(attrs={"id":"shopCode","name":"shopCode","readonly":"readonly"}),max_length=1000,
                               required=False)
    proCode = forms.CharField(widget=forms.TextInput(attrs={"name":"proCode"}),max_length=20,required=False)
    barcode = forms.CharField(widget=forms.TextInput(attrs={"name":"barcode"}),max_length=20,required=False)
    num1 = forms.FloatField(widget=forms.TextInput(attrs={"name":"num1","value":"0"}),required=True,error_messages={"required":"库存范围为必填"})
    num2 = forms.FloatField(widget=forms.TextInput(attrs={"name":"num2","value":"100000"}),required=True,error_messages={"required":"库存范围为必填"})
    scCode = forms.CharField(widget=forms.TextInput(attrs={"name":"scCode"}),max_length=20,required=False)
    proName = forms.CharField(widget=forms.TextInput(attrs={"name":"proName"}),max_length=64,required=False)
    ORDER_CHOICES = (
        ('sccode', u'小类编码'),
        ('procode', u'商品编码'),
        ('proname', u'商品名称'),
        ('num', u'库存数量'),
    )
    orderStyle = forms.ChoiceField(widget=forms.Select(attrs={"name":"orderStyle",}),choices=ORDER_CHOICES)