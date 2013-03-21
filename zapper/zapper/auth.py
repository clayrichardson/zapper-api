
from django.contrib.auth.models import User
from django.middleware.csrf import _sanitize_token, constant_time_compare
from django.utils.http import same_origin
from django.conf import settings

from tastypie.http import HttpUnauthorized
from tastypie.authentication import Authentication
from tastypie.authentication import SessionAuthentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

from zapper.models import ApiKey

import logging
logger = logging.getLogger(__name__)

class ZapperAuthentication(ApiKeyAuthentication):

    def extract_credentials(self, request, fields=[]):
        return_fields = {}
        for field in fields:
            return_fields[field] = request.GET.get(field) or request.POST.get(field)
        logger.debug('fields: %s' % (return_fields))
        return return_fields

    def get_key(self, user, password):
        if not user.check_password(password):
            logger.debug('password incorrect: %s' % (user))
            return False
        else:
            logger.debug('password correct: %s' % (user.email))
            return True

    def get_user(self, email):
        try:
            user = User.objects.get(email=email)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            logger.debug('user does not exist')
            return False

        if not user or not self.check_active(user):
            logger.debug('no user or user inactive')
            return False

        return user

    def key_auth_check(self, request, user, password):
        key = self.get_key(user, password)
        if key and not isinstance(key, HttpUnauthorized):
            self.set_request_user(request, user)
            return True
        return False

    def set_request_user(self, request, user):
        request.user = user

    def get_identifier(self, request):
        logger.debug('get_identifier: %s' % (request.user.username))
        return request.user.username

class ZapperUserAuthentication(ZapperAuthentication):

    def is_authenticated(self, request, **kwargs):
        try:
            fields = ['email', 'password']
            field = self.extract_credentials(request, fields)
            logger.debug('field: %s' % (field))
        except ValueError:
            return self._unauthorized()

        if not field['email'] or not field['password']:
            logger.debug('no email or password provided')
            return self._unauthorized()

        user = self.get_user(field['email'])

        if self.key_auth_check(request, user, field['password']):
            return True

        return self._unauthorized()

class ZapperApiKeyAuthentication(ZapperAuthentication):
    def is_authenticated(self, request, **kwargs):
        try:
            fields = ['email', 'password', 'key', 'secret']
            field = self.extract_credentials(request, fields)
        except ValueError:
            return self._unauthorized()

        try:
            apikey = ApiKey.objects.get(
                    key = field['key'],
                    secret = field['secret'],
                    enabled = True
                    )
            if apikey.key != field['key']:
                logger.debug('key incorrect: %s' % (user))
                return self._unauthorized()
            logger.debug('key correct: %s' % (apikey.key))
            if apikey.secret != field['secret']:
                logger.debug('secret incorrect: %s' % (user))
                return self.unauthorized()
            logger.debug('secret correct: %s' % (apikey.secret))

        except ApiKey.DoesNotExist:
            logger.debug('key does not exist: %s' % (user))
            return self._unauthorized()

        user = self.get_user(field['email'])

        if self.key_auth_check(request, user, field['password']):
            return True
        return self._unauthorized()

    def get_identifier(self, request):
        return request.user.username

class ZapperSessionAuthentication(SessionAuthentication):
    def is_authenticated(self, request, **kwargs):

        logger.debug('cookie name: %s' % (settings.CSRF_COOKIE_NAME))
        csrf_token = _sanitize_token(request.COOKIES.get(settings.CSRF_COOKIE_NAME, ''))
        logger.debug('csrf_token: %s' % (csrf_token))

        if request.is_secure():
            referer = request.META.get('HTTP_REFERER')

            if referer is None:
                logger.debug('referer is none')
                return False

            good_referer = 'https://%s/' % (request.get_host())

            if not same_origin(referer, good_referer):
                logger.debug('not same origin')
                return False

        if request.META.get('CSRF_COOKIE_USED', ''):
            logger.debug('csrf cookie used')
            request_csrf_token = request.META.get('CSRF_COOKIE', '')
        else:
            logger.debug('csrf cookies not used, using http_x_csrftoken')
            request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

        logger.debug('request_csrf_token: %s' % (request_csrf_token))

        if not constant_time_compare(request_csrf_token, csrf_token):
            logger.debug('not constant time compare')
            return False

        logger.debug('session auth returning true')
        return True

class ZapperAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        logger.debug('user id: %s' % (bundle.request.user.id))
        return object_list.filter(owner=bundle.request.user.id)

    def read_detail(self, object_list, bundle):
        logger.debug('user pk: %s' % (bundle.request.user.id))
        if bundle.obj.owner != bundle.request.user:
            raise Unauthorized("You are not allowed to access that resource.")
        return True

