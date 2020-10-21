from django.conf.urls import patterns, include, url
#from page import views

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^kd-admin/', include('wp_admin.urls')),
    url(r'^', include('page.urls')), 
    url(r'^admin/', include(admin.site.urls)),   
    url(r'^event-on/', include('eventon.urls')),
    #url(r'^services/', include('service.urls')),
    #url(r'^snippets/', include('snippets.urls')),
    url(r'^services/', include('restservices.urls')),
)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}),
)
