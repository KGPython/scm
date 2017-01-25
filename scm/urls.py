"""scm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': root_path+'/static/css'}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': root_path+'/static/javascript'}),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root':root_path+ '/static/image'}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': root_path + '/static/fonts'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scm/',include("base.urls")),
]

