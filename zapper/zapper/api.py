from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from zapper.auth import UserAuthentication

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = UserAuthentication()
        excludes = ['email', 'password']
