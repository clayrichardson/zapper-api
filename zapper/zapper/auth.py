from django.contrib.auth.models import User
from tastypie.authentication import Authentication

from zapper.models import ApiKey

import logging
logger = logging.getLogger(__name__)

class UserAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        try:
            email = request.REQUEST['email']
            password = request.REQUEST['password']
            logger.debug('email, password: %s, %s' % (email, password))
        except KeyError:
            return False

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                logger.debug('found user: %s' % (user))
                return True
            else:
                return False
        except User.DoesNotExist:
            logger.debug('user does not exist: %s' %(user))
            return False

class ZapperAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        try:
            email = request.REQUEST['email']
            password = request.REQUEST['password']
            key = request.REQUEST['key']
            secret = request.REQUEST['secret']
            logger.debug(
                    'email, password, key, secret: %s, %s, %s, %s' %
                    (email, password, key, secret)
            )
        except KeyError:
            return False

        try:
            user = User.objects.get(email=email)
            apikey = ApiKey.objects.get(
                    key = key,
                    secret = secret,
                    enabled = True
                    )
            if not user.check_password(password):
                logger.debug('password incorrect: %s' % (user))
                return False
            if apikey.key != key:
                logger.debug('key incorrect: %s' % (user))
                return False
            if apikey.secret != secret:
                logger.debug('secret incorrect: %s' % (user))
                return False
            return True
        except User.DoesNotExist:
            logger.debug('user does not exist: %s' % (user))
            return False
        except ApiKey.DoesNotExist:
            logger.debug('key does not exist: %s' % (user))
            return False
            
