from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('apps.social.views',
    url(r"^connect_with/(?P<service>\w+)/$", "connect", name="oauth_access_login"),
    url(r"^callback/(?P<service>\w+)/$", "callback", name="oauth_access_callback"),
    url(r"^disconnect/(?P<service>\w+)/$", "disconnect", name="oauth_disconnect"),
)