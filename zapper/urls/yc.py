
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'zapper.views.yc_landing_page'),
)

