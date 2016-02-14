# -*- coding:utf-8 -*-
__author__ = 'End-e'
from django import forms
from base.models import BasUser, BasUserRole, BasGroup


class ChangeGrpPass(forms.Form):
    #grpcode = forms.CharField(widget=forms.TextInput(attrs={"id": "grpCode", "name": "grpCode"}), max_length=20)
    ucode = forms.CharField(widget=forms.TextInput(attrs={"id": "uCode", "name": "uCode"}),required=True,
                              error_messages={"required": "请填写用户"},max_length=20)
    passwd = forms.CharField(widget=forms.PasswordInput(),required=True,error_messages={"required": "请填写新密码"}, max_length=50)
    confirmpass = forms.CharField(widget=forms.PasswordInput(), required=True, error_messages={"required": "请输入确认密码"},
                                  max_length=50)

    def clean_confirmpass(self):
        if 'passwd' in self.cleaned_data:
            password1 = self.cleaned_data['passwd']
            password2 = self.cleaned_data['confirmpass']
            if password1 == password2:
                return password2
            raise forms.ValidationError('密码不匹配')