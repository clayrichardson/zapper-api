
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

import logging
logger = logging.getLogger(__name__)

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

