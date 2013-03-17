
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api

from zapper.api import ApiKeyResource
from zapper.api import FileResource
from zapper.api import UserResource

v1_api = Api(api_name = 'v1')
v1_api.register(ApiKeyResource())
v1_api.register(FileResource())
v1_api.register(UserResource())


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),

    url(r'^$', 'zapper.views.landing_page'),
)
