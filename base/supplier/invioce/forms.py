__author__ = 'Administrator'
from django import forms

class invoiceDetailForm(forms.Form):
    CCLASS_CHOICES=(('0',u'收据'),('1',u'普票'),('2',u'税票'))
    cclass = forms.ChoiceField(widget=forms.Select(),choices=CCLASS_CHOICES)
    ctaxrate = forms.IntegerField(max_value=100,min_value=0)
    cno = forms.CharField(max_length=10)
    cmoney = forms.DecimalField(max_digits=12, decimal_places=2)
    csh = forms.DecimalField(max_digits=10, decimal_places=2)
    jshj = forms.DecimalField(max_digits=12, decimal_places=2)
    kmoney = forms.DecimalField(max_digits=12, decimal_places=2)
    sjfk = forms.DecimalField(max_digits=12, decimal_places=2)
    PAYTYPE_CHOICES=(('0',u'支票'),('1',u'电汇'),('2',u'汇票'),('3',u'网银'),('4',u'其他'))
    paytype= forms.ChoiceField(widget=forms.Select(),choices=PAYTYPE_CHOICES)
    cdate = forms.DateTimeField()
    cdno = forms.CharField(max_length=20)
    cgood = forms.CharField(max_length=40)