
import json

from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from zapper.models import ApiKey
from zapper.models import File

import logging

logger = logging.getLogger(__name__)

class FileResourceTest(ResourceTestCase):
    fixtures = ['users', 'apikeys', 'files']

    def setUp(self):
        super(FileResourceTest, self).setUp()

        self.apikey = ApiKey.objects.get(enabled=True)
        self.data = {
            'email': 'user1@user.com',
            'password': 'user1password',
            'key': self.apikey.key,
            'secret': self.apikey.secret,
        }

    def test_get_list(self):
        data = self.data

        response = self.api_client.get(
            '/api/v1/file/',
            format = 'json',
            data = data,
        )

        self.assertValidJSONResponse(response)
    
    def test_read_list_filter(self):
        data = self.data

        response = self.api_client.get(
            '/api/v1/file/',
            format = 'json',
            data = data,
        )

        self.assertValidJSONResponse(response)
        json_objects = self.deserialize(response)

        user = User.objects.get(email=data['email'])

        for file_object in json_objects['objects']:
            self.assertEqual(user.pk, file_object['id'])

    def test_read_detail_filter(self):
        data = self.data

        response = self.api_client.get(
            '/api/v1/file/1/',
            format = 'json',
            data = data,
        )

        self.assertValidJSONResponse(response)

    def test_read_detail_filter_unauthorized(self):
        data = self.data

        response = self.api_client.get(
            '/api/v1/file/2/',
            format = 'json',
            data = data,
        )

        logger.debug('response: %s' % (response))
        self.assertHttpNotFound(response)

