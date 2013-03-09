from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        authentication = ApiKeyAuthentication()
