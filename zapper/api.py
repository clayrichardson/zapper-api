
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer

from zapper.auth import ZapperSessionAuthentication

from zapper.models import *

import logging

logger = logging.getLogger(__name__)

class WaitListResource(ModelResource):
     class Meta:
         queryset = WaitList.objects.all()
         allowed_methods = ['post']
         include_resource_uri = False
         authentication = ZapperSessionAuthentication()
         authorization = Authorization()
         serialization = Serializer(formats=['json'])

     def wrap_view(self, view):
         @ensure_csrf_cookie
         def wrapper(request, *args, **kwargs):
             wrapped_view = super(WaitListResource, self).wrap_view(view)
             return wrapped_view(request, *args, **kwargs)
         return wrapper

