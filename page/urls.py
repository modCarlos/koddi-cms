from django.conf.urls import patterns, include, url
#from page import page.views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.page.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'page.views.index', name='index'),
    url(r'^courses/', 'page.views.courses', name='courses'),
    url(r'^tutoriales/', 'page.views.tutoriales', name='tutoriales'),
    url(r'^post/(?P<slug_post>\S+)/', 'page.views.post', name='post'),
    url(r'^course/(?P<slug_course>\S+)/', 'page.views.course', name='course'),
    url(r'^category/(?P<slug_category>\S+)/', 'page.views.category', name='category'),
    url(r'^tag/(?P<slug_tag>\S+)/', 'page.views.tag', name='tag'),
    url(r'^author/(?P<username>\w+)/posts/', 'page.views.author_posts', name='author_posts'),
    url(r'^author/(?P<username>\w+)/', 'page.views.author', name='author'),

    url(r'^auth/login/', 'page.views.login', name='login'),
    url(r'^auth/register/', 'page.views.register', name='register'),
    url(r'^auth/password/change/', 'page.views.change_password', name='change_password'),
    url(r'^auth/logout/', 'page.views.logout', name='logout'),
    url(r'^profile/', 'page.views.profile', name='logout'),
    url(r'^profile/edit/', 'page.views.edit_profile', name='edit_profile'),
    url(r'^contact-us/', 'page.views.contact', name='contact'),
    url(r'^search/', 'page.views.search', name='search'),
    url(r'^about/', 'page.views.about', name='about'),
    url(r'^add_favorite/', 'page.views.add_favorite', name='add_favorite'),
    url(r'^remove_favorite/', 'page.views.remove_favorite', name='remove_favorite'),

    #Facebook connect
    url(r'^facebook/$', 'page.views.facebook'),

    #reset password
	#Reset password
    url(r'^accounts/password/reset/$', 'page.views.reset' , name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'page.views.reset_confirm' , name='password_reset_confirm'),
    url(r'^success/$', 'page.views.success', name='success'),

    #Payments Stripe - Paypal - etc
    url(r'^payment_details/(?P<payment_id>\S+)/$', 'page.views.payment_details'),
    url('^payments/', include('payments.urls')),
    url('^checkout/', 'page.views.checkout'),
    url('^cart/', 'page.views.cart'),
)
