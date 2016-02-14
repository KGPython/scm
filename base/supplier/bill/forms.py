# -*- coding:utf-8 -*-
from django import forms

class BillInForm(forms.Form):
    shopcode = forms.CharField(widget=forms.TextInput(attrs={"id":"shopCode","name":"shopCode","readonly":"readonly"}),
                               required=False)
    code = forms.CharField(widget=forms.TextInput(attrs={"id":"code","name":"code"}),required=False)
    start = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"start","name":"start"}),required=True,error_messages={"required":"起始日期不能为空",})
    end = forms.DateField(widget=forms.DateInput(attrs={"class":"inline laydate-icon","id":"end","name":"end"}),required=True,error_messages={"required":"截止日期不能为空",})


class AdPriceForm(BillInForm):
    CHIOCE_LIST=(("chdate",u"审核日期"),("shopcode",u"门店"))
    orderStyle = forms.ChoiceField(widget=forms.Select(attrs={"name":"orderStyle"}),choices=CHIOCE_LIST)

class form1(forms.Form):
    aa = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())