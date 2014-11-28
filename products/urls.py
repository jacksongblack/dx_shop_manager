from django.conf.urls import patterns, url
from products import views

urlpatterns = patterns('',
    # url(r'^blog/', include('blog.urls')),
    url(r'^create/$',views.ProductController().create,name="pro"),
    url(r'^index/$',views.ProductController().index,name="index"),
    url(r'^show/(?P<id>\w+)/$',views.ProductController().show,name="show"),
    url(r'^delete/(?P<id>\w+)/$',views.ProductController().show,name="show"),
    url(r'^update/(?P<id>\w+)/$',views.ProductController().update,name="update"),
)
