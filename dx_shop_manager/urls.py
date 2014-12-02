from django.conf.urls import patterns, include, url

from django.contrib import admin
from dx_shop_manager import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'dx_bdos.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^user/', include('users.urls', namespace='users')),
                       url(r'^api/user/', include('users.api.urls', namespace='userApi')),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^product/', include('products.urls')),
                       url(r'^categories/', include('categories.urls')),
                       url(r'^onlineEdit/', include('onlineEdit.urls')),
                       url(r'ueEditorControler', 'onlineEdit.controller.handler'),
                       url( r'^upload/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': (settings.BASE_DIR + "/upload").replace('\\', '/')}
                       ),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)