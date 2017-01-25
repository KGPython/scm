#-*- coding:utf-8 -*-
from django.conf.urls import url
urlpatterns = [
    url(r'^index/$','base.rbac.index.index',name='rbac'),
    url(r'^role/index/$','base.rbac.role.index.index',name='rbacRole'),
    url(r'^role/create/$','base.rbac.role.create.index',name='rbacRoleCreate'),

    url(r'^role/info/$','base.rbac.role.info.index',name='rbacRole'),
    url(r'^role/info/save/$','base.rbac.role.info.save',name='rbacSave'),
    url(r'^role/info/show/$','base.rbac.role.info.show',name=''),
]