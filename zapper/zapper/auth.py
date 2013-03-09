from django.contrib.auth.models import User
from tastypie.authentication import Authentication

class UserAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        try:
            email = request.REQUEST['email']
            password = request.REQUEST['password']
        except KeyError:
            return False

        try:
            user_model = User.objects.get(username=email)
            if user_model.check_password(password):
                return True
            else:
                return False
        except User.DoesNotExist:
            return False
