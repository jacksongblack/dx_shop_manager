from django.conf.urls import patterns, url
from categories import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^create/$', login_required(views.CategoriesController().create, login_url="/user/login/"),
                           name="pro"),
                       url(r'^index/$', login_required(views.CategoriesController().index, login_url="/user/login/"),
                           name="index"),
                       # url(r'^show/(?P<id>\w+)/$',
                       #     login_required(views.CategoriesController().show, login_url="/user/login/"), name="show"),
                       url(r'^delete/(?P<id>\w+)/$',
                           login_required(views.CategoriesController().delete, login_url="/user/login/"), name="delete"),
                       # url(r'^update/(?P<id>\w+)/$',
                       #     login_required(views.CategoriesController().update, login_url="/user/login"), name="update"),
)
