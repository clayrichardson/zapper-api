
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from zapper.api import WaitListResource

v1_api = Api(api_name = 'v1')
v1_api.register(WaitListResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', 'zapper.views.landing_page'),
    url(r'^waitlist$', 'zapper.views.wait_list'),
)
