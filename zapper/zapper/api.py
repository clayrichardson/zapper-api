
from psycopg2 import IntegrityError
from django.contrib.auth.models import User
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from zapper.auth import ZapperAuthorization
from zapper.auth import ZapperUserAuthentication
from zapper.auth import ZapperApiKeyAuthentication
from zapper.models import *

import logging

logger = logging.getLogger(__name__)

class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.filter(enabled=True)
        authentication = ZapperUserAuthentication()

class FileResource(ModelResource):
    class Meta:
        queryset = File.objects.all()
        authentication = ZapperApiKeyAuthentication()
        authorization = ZapperAuthorization()

    def get_object_list(self, bundle, request=None, **kwargs):
        return super(FileResource,
            self).get_object_list(bundle).filter(
            owner=bundle.user.id
        )

    def obj_create(self, bundle, **kwargs):
        return super(FileResource, self).obj_create(
            request, user=request.user
        )

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

