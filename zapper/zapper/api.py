
from tastypie.resources import ModelResource
from zapper.auth import UserAuthentication
from zapper.models import *

class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.filter(enabled=True)
        authentication = UserAuthentication()

class FileResource(ModelResource):
    class Meta:
        queryset = File.objects.filter()

