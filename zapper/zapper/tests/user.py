
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from zapper.models import ApiKey

import logging

logger = logging.getLogger(__name__)

class UserResourceTest(ResourceTestCase):
    fixtures = ['users', 'apikeys']

    def setUp(self):
        super(UserResourceTest, self).setUp()

    def test_post_new_user(self):
        post_data = {
            'email': 'new@user.com',
            'password': 'newpassword',
            'first_name': 'newfirstname',
            'last_name': 'newlastname',
        }
        number_users = User.objects.count()
        response = self.api_client.post(
            '/api/v1/user/',
            format = 'json',
            data = post_data,
        )
        self.assertHttpCreated(response)
        number_users += 1
        self.assertEqual(number_users, User.objects.count())

