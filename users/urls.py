from django.conf.urls import patterns, url

from django.contrib import admin
from users import views
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^login/$',views.login,name = 'login'),
     url(r'create/$,',views.create,name="logging"),
     url(r'^(?P<pk>\w+)/$',login_required(views.Userdetail.as_view()),name='detail'),
)
