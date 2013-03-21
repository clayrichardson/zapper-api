
from django.test import Client

from tastypie.test import ResourceTestCase

from zapper.models import WaitList

import logging

logger = logging.getLogger(__name__)

class WaitListResourceTest(ResourceTestCase):

    def setUp(self):
        super(WaitListResourceTest, self).setUp()

    def test_post_new_email(self):
        post_data = {
            'email': 'new@user.com',
        }
        waitlist_length = WaitList.objects.count()
        logger.debug('waitlist_length: %s' % (waitlist_length))
        response = self.api_client.get('/api/v1/waitlist', follow=True)
        logger.debug('test get response: %s' % (response))
        response = self.api_client.post(
            '/api/v1/waitlist/',
            format = 'json',
            data = post_data,
        )
        logger.debug('response: %s' % (response))
        self.assertHttpCreated(response)
        waitlist_length += 1
        logger.debug('waitlist_length: %s' % (waitlist_length))
        self.assertEqual(waitlist_length, WaitList.objects.count())

