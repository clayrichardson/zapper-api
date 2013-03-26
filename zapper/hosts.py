
from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'.*yc.*', 'zapper.urls.yc', name='yc'),
    host(r'(\w+)', settings.ROOT_URLCONF, name='wildcard'),
)

