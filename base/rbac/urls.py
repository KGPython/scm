#-*- coding:utf-8 -*-
from django.conf.urls import url
urlpatterns = [
    url(r'^index/$','base.rbac.index.index',name='rbac'),

    url(r'^role/index/$','base.rbac.role.view.index',name='rbacRole'),
    url(r'^role/create/$','base.rbac.role.view.create',name='rbacRoleCreate'),
    url(r'^role/create/$','base.rbac.role.view.delete',name='rbacRoleDel'),
    url(r'^role/info/$','base.rbac.role.view.info',name='rbacRoleInfo'),
    url(r'^role/info/save/$','base.rbac.role.view.infoSave',name='rbacRoleInfoSave'),


    url(r'^user/index/$','base.rbac.user.view.index',name='rbacUser'),
    url(r'^user/create/$','base.rbac.user.view.create',name='rbacUserCreate'),
    url(r'^user/del/$','base.rbac.user.view.delete',name='rbacUserDel'),
    url(r'^user/info/$','base.rbac.user.view.info',name='rbacUserInfo'),
]