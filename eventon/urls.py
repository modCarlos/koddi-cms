from django.conf.urls import patterns, include, url
#from eventon.eventon.views import *
#from eventon import views
from api import UserResource, EventResource, PostResource, CreateUserResource
from django.contrib import admin
from tastypie.api import Api
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.eventon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'eventon.views.index', name='index'),
    url(r'^events/$', 'eventon.views.events', name='events'),
    url(r'^event/(?P<slug>\S+)/$', 'eventon.views.event', name='event'),
    url(r'^categories/$', 'eventon.views.categories', name='categories'),
    url(r'^category/(?P<slug>\S+)/$', 'eventon.views.category', name='category'),
    url(r'^calendar/$', 'eventon.views.calendar', name='calendar'),

    url(r'^post/(?P<slug>\S+)/buy-ticket/$', 'eventon.views.buy_ticket', name='buy_ticket'),
    url(r'^post/(?P<slug>\S+)/$', 'eventon.views.post', name='post'),
    url(r'^tag/(?P<slug>\S+)/$', 'eventon.views.tag', name='tag'),

    # More urls
    url(r'^profile/$', 'eventon.views.profile', name='profile'),
    url(r'^profile/edit/$', 'eventon.views.edit_profile', name='edit_profile'),
    url(r'^profile/wishlist/$', 'eventon.views.wishlist', name='wishlist'),
    url(r'^profile/boughts/$', 'eventon.views.boughts', name='boughts'),
    url(r'^profile/upgrade/$', 'eventon.views.upgrade', name='upgrade'),
    
    url(r'^auth/login/$', 'eventon.views.login', name='login'),
    url(r'^auth/register/$', 'eventon.views.register', name='register'),
    url(r'^auth/logout/$', 'eventon.views.logout', name='logout'),
    url(r'^search/$', 'eventon.views.search', name='search'),
    url(r'^post/create/$', 'eventon.views.create_post', name='create_post'),
    url(r'^wishlist/add/$', 'eventon.views.add_to_wishlist', name='add_to_wishlist'),

    url(r'^comment/$', 'eventon.views.comment', name='comment'),
    #Facebook connect
    url(r'^facebook/$', 'eventon.views.facebook', name='facebook'),

    #Reset password
    url(r'^accounts/password/reset/$', 'eventon.views.reset' , name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'eventon.views.reset_confirm' , name='password_reset_confirm'),
    url(r'^success/$', 'eventon.views.success', name='success'),

    ##Some for paypal account 

    #Contact
    #About
    #Google analitics
)

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EventResource())
v1_api.register(PostResource())
v1_api.register(CreateUserResource())
#category_resource = CategoryResource()

urlpatterns += patterns('',
	url(r'^api/', include(v1_api.urls)),
)