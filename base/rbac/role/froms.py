# -*-  coding:utf-8 -*-
from django import forms
from base.models import RbacShop,BasOrg,RbacMoudle


def getDeparts(id):
    departs = RbacShop.objects.values('shopcode','shopnm').filter(shoptype=id,enable=1)
    data = set()
    for depart in departs :
        data.add((depart['shopcode'],depart['shopnm']))
    return data

def getClasses(id):
    classes = BasOrg.objects.values('orgcode','orgname').filter(tier=2,parentcode=id)
    data = set()

    for obj in classes:
        data.add((obj['orgcode'],obj['orgname']))
    return data

def getModules(id):
    modulesChild = RbacMoudle.objects.values('m_name','m_id').filter(status=1,p_id=id)
    data = set()
    for c in modulesChild:
        data.add((c['m_id'],c['m_name']))
    return data


class roleInfoForm(forms.Form):
    chaoShi = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getDeparts(11))
    baiHuo = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getDeparts(12))
    bianLiDian = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getDeparts(13))

    shengXian = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getClasses(1))
    shiPin = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getClasses(2))
    feiShi = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getClasses(3))
    jiaDian = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getClasses(4))
    yunYing = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getClasses(6))

    dailyCHSH = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getModules(1))
    dailyBH = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getModules(2))
    dailyBLD = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getModules(3))
    dailyErr = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=getModules(4))


from django import forms
from django.forms.extras.widgets import SelectDateWidget

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
                            ('green', 'Green'),
                            ('black', 'Black'))

class SimpleForm(forms.Form):
    birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)


