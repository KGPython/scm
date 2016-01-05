# -*- coding:utf-8 -*-
__author__ = 'End-e'
from django import forms
from base.models import BasRole


class RoleForm(forms.Form):
    nm = forms.CharField(widget=forms.TextInput(attrs={"id": "uName", "name": "uName"}), required=True,
                         error_messages={"required": "请填写名称", }, max_length=50)
    rcode = forms.CharField(widget=forms.TextInput(attrs={"id": "uId", "name": "uId"}), required=True,
                            error_messages={"required": "请填写编号", }, max_length=20)
    CHOICES = (('0', '无效',), ('1', '有效',))
    status = forms.ChoiceField(widget=forms.Select(attrs={"id": "uStatus", "name": "uStatus"}), required=True,
                               error_messages={"required": "请选择状态", }, choices=CHOICES)
    remark = forms.CharField(widget=forms.TextInput(attrs={"id": "uRemark", "name": "uRemark"}), max_length=10,
                             required=False)
    grpcode = forms.CharField(widget=forms.TextInput(attrs={"id": "uCompany", "name": "uCompany"}), max_length=20,
                              required=False)
