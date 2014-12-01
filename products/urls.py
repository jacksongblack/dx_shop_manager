from django.conf.urls import patterns, url
from products import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # url(r'^blog/', include('blog.urls')),
    url(r'^create/$',login_required(views.ProductController().create,login_url="/user/login/"),name="pro"),
    url(r'^index/$',login_required(views.ProductController().index,login_url="/user/login/"),name="index"),
    url(r'^show/(?P<id>\w+)/$',login_required(views.ProductController().show,login_url="/user/login/"),name="show"),
    url(r'^delete/(?P<id>\w+)/$',login_required(views.ProductController().show,login_url="/user/login/"),name="show"),
    url(r'^update/(?P<id>\w+)/$',login_required(views.ProductController().update,login_url="/user/login"),name="update"),
)
