
from psycopg2 import IntegrityError
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from zapper.auth import UserAuthentication
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

class UserResource(ModelResource):
    class Meta:
        object_class = User
        queryset = User.objects.all()
        allowed_methods = ['post']
        include_resource_uri = False
        excludes = ['password']
        authentication = Authentication()
        authorization = Authorization()

    def obj_create(self, bundle, **kwargs):
        try:
            bundle = super(UserResource, self).obj_create(
                bundle, **kwargs
            )
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('The username already exists')
        return bundle

