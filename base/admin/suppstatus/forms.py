# -*- coding:utf-8 -*-
__author__ = 'End-e'
from django import forms
from base.models import BasFee, BasSupplier, BasGroup, BasRole


class SuppQuery(forms.Form):
    bid = forms.CharField(widget=forms.TextInput(attrs={"id": "bid", "name": "bid"}), required=False)
    suppcode = forms.CharField(widget=forms.TextInput(attrs={"id": "suppcode", "name": "suppcode"}), required=False,
                               max_length=20)
    status = forms.ChoiceField(widget=forms.Select(attrs={"name": "status"}), choices=(('', '全部'),('N', '已禁用'), ('Y', '已启用')))


class SuppStatusForm(forms.Form):
    status = forms.ChoiceField(widget=forms.Select(attrs={"name": "status"}), choices=(('N', '禁用'), ('Y', '启用')))
    bsum = forms.DecimalField(widget=forms.TextInput(attrs={"name": "bsum"}), required=False, max_digits=16,
                              decimal_places=4)
    bid = forms.CharField(widget=forms.TextInput(attrs={"id": "bids", "name": "bid"}), required=False)
    ucode = forms.CharField()
    grpcode = forms.CharField()
    suppcode = forms.CharField()
    begindate = forms.DateField()
    enddate = forms.DateField()
    remark = forms.CharField(required=False)