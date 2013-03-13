
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from zapper.api import ApiKeyResource

v1_api = Api(api_name = 'v1')
v1_api.register(ApiKeyResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'zapper.end_points.access.login'),
    url(r'^api/', include(v1_api.urls)),
)
