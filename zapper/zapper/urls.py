from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'zapper.end_points.access.login'),

    url(r'^$', 'zapper.views.check_login'),
)
