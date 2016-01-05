# -*- coding:utf-8 -*-
__author__ = 'End-e'
from django import forms
from base.models import BasUser, BasUserRole, BasGroup


class ChangeGrpPass(forms.Form):
    grpcode = forms.CharField(widget=forms.TextInput(attrs={"id": "grpCode", "name": "grpCode"}), required=True,
                              error_messages={"required": "请填写编号", }, max_length=20)
    ucode = forms.CharField(widget=forms.TextInput(attrs={"id": "uCode", "name": "uCode"}), required=False,
                            max_length=20)
    passwd = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    confirmpass = forms.CharField(widget=forms.PasswordInput(), required=True, error_messages={"required": "请再次输入密码"},
                                  max_length=50)

    # def clean_passwd(self):
    #     if 'passwd' in self.cleaned_data:
    #         passwd = self.cleaned_data['passwd']
    #         confirmpass = self.cleaned_data['confirmpass']
    #         if passwd == confirmpass:
    #             return confirmpass
    #         raise forms.ValidationError('密码输入不一致')