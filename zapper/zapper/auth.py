from django.contrib.auth.models import User
from tastypie.authentication import Authentication

from zapper.models import ApiKey

class UserAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        try:
            email = request.REQUEST['email']
            password = request.REQUEST['password']
        except KeyError:
            return False

        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                return True
            else:
                return False
        except User.DoesNotExist:
            return False

class ZapperAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        try:
            email = request.REQUEST['email']
            password = request.REQUEST['password']
            key = request.REQUEST['key']
            secret = request.REQUEST['secret']
        except KeyError:
            return False

        try:
            user = User.objects.get(username=email)
            apikey = ApiKey.objects.get(
                    key = key,
                    secret = secret,
                    enabled = True
                    )
            if not user.check_password(password): return False
            if apikey.key != key: return False
            if apikey.secret != secret: return False
            return True
        except User.DoesNotExist:
            return False
        except ApiKey.DoesNotExist:
            return False
            
