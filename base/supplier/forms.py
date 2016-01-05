#-*- coding:utf-8 -*-
__author__ = 'liubf'

from django import forms

class ChangepwdForm(forms.Form):

    newpassword = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"新密码",
            }
        ),
    )
    repassword = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
            }
        ),
    )

    def clean_form(self):

        newPwd = self.cleaned_data['newpassword']
        if len(newPwd)<6:
            raise forms.ValidationError(u"密码长度不能小于6")

        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword'] != self.cleaned_data['repassword']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data