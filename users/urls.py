from django.conf.urls import patterns, url

from django.contrib import admin
from users import views
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^login/$',views.login,name = 'login'),
     url(r'^logout/$',views.logout,name = 'logout'),
     url(r'^create/$',login_required(views.UserControll().create),name="create"),
     url(r'^update/(?P<id>w+)$',login_required(views.UserControll().update),name="update"),
     url(r'^(?P<pk>w+)/$',login_required(views.Userdetail.as_view()),name='detail'),
)
