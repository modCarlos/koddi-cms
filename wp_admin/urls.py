from django.conf.urls import patterns, include, url
from wp_admin import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^users/$', views.users, name='users'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^payments/$', views.payments, name='payments'),

    #ADD
    url(r'^add_course/$', views.add_course, name='add_course'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    url(r'^add_superuser/$', views.add_superuser, name='add_superuser'),

    url(r'^course/(?P<slug>\S+)/edit/$', views.edit_course, name='edit_course'),
    url(r'^post/(?P<slug>\S+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^tag/(?P<slug>\S+)/edit/$', views.edit_tag, name='edit_tag'),
    url(r'^category/(?P<slug>\S+)/edit/$', views.edit_category, name='edit_category'),
    url(r'^user/(?P<slug>\S+)/edit/$', views.edit_user, name='edit_user'),
    # url(r'^blog/', include('blog.urls')),

    #Delete
    url(r'^course/(?P<slug>\S+)/delete/$', views.del_course, name='del_course'),
    url(r'^post/(?P<slug>\S+)/delete/$', views.del_post, name='del_post'),
    url(r'^tag/(?P<slug>\S+)/delete/$', views.del_tag, name='del_tag'),
    url(r'^category/(?P<slug>\S+)/delete/$', views.del_category, name='del_category'),

)
