from django.conf.urls import patterns, url

from django.contrib import admin
from users import views
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^create/$', views.UserControll().create, name="create"),
                       url(r'^update/(?P<id>w+)/$',
                           login_required(views.UserControll().update, login_url="/user/login/"), name="update"),
                       url(r'^show/(?P<id>\w+)/$',
                           login_required(views.UserControll().show, login_url="/user/login/"), name="show"),
                       url(r'^index/$', login_required(views.UserControll().index, login_url="/user/login/"),
                           name="update"),
                       url(r'^(?P<pk>w+)/$', login_required(views.Userdetail.as_view(), login_url="/user/login/"),
                           name='detail'),
)
