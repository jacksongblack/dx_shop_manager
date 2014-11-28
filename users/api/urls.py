#coding=utf-8
'''
Created on 2014年8月10日
登录api url配置
@author: tubin
'''
from django.conf.urls import patterns, url
from django.contrib import admin
from users.api import views
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^login/$', views.Login.as_view()),
     url(r'^logout/$', views.Logout.as_view()),
)
