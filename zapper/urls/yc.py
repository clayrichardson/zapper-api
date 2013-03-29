
from django.conf.urls import patterns, include, url

from tastypie.api import Api

from zapper.api import WaitListResource

v1_api = Api(api_name = 'v1')
v1_api.register(WaitListResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', 'zapper.views.yc_landing_page'),
)

