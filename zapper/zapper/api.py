
from tastypie.resources import ModelResource
from zapper.auth import UserAuthentication
from tastypie.authorization import Authorization
from zapper.models import *

import logging

logger = logging.getLogger(__name__)

class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.filter(enabled=True)
        authentication = UserAuthentication()

class FileResource(ModelResource):
    class Meta:
        queryset = File.objects.all()
        authentication = UserAuthentication()

    def obj_create(self, bundle, request=None, **kwargs):
        logger.debug('bundle: %s' % (bundle))
        logger.debug('request: %s' % (request))
        return super(FileResource, self).obj_create(bundle, request, user=request.user)

    def apply_authorization_limits(self, request, object_list):
        return object_list.filter(user=request.user)
