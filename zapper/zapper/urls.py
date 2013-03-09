from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from zapper.api import UserResource

user_resource = UserResource()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
