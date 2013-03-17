
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from zapper.models import ApiKey

import logging

logger = logging.getLogger(__name__)

class ApiKeyResourceTest(ResourceTestCase):
    fixtures = ['users', 'apikeys']

    def setUp(self):
        super(ApiKeyResourceTest, self).setUp()

        self.user1 = User.objects.get(username='user1')

    def test_authentication(self):
        post_data = {
            'email': 'user1@user.com',
            'password': 'user1password',
        }
        response = self.api_client.get(
            '/api/v1/apikey/',
            format = 'json',
            data = post_data,
        )
        logger.debug('response: %s' % (response))
        self.assertValidJSONResponse(response)

