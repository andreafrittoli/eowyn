# Copyright 2015 Andrea Frittoli <andrea.frittoli@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from eowyn import api
from eowyn.model import manager
from eowyn.tests import base


def cleanup_message(message):
    return message.rstrip('\n"').lstrip('"')


class TestRestAPI(base.TestCase):

    def setUp(self):
        super(TestRestAPI, self).setUp()
        api.app.config['TESTING'] = True
        api.manager = manager.get_manager()
        self.app = api.app.test_client()

    def test_subscription_get(self):
        self.app.post('/topic/username')
        self.app.post('/topic', data='message',
                      headers={"content-type": "text/plain"})
        response = self.app.get('/topic/username')
        self.assertEqual(200, response.status_code)
        self.assertEqual('message', cleanup_message(response.data))

    def test_subscription_get_many_messages(self):
        messages = ['first_message', 'second_message']
        self.app.post('/topic/username')
        for message in messages:
            self.app.post('/topic', data=message,
                          headers={"content-type": "text/plain"})
        for expected in messages:
            response = self.app.get('/topic/username')
            self.assertEqual(200, response.status_code)
            self.assertEqual(expected, cleanup_message(response.data))

    def test_subscription_get_no_message(self):
        self.app.post('/topic/username')
        response = self.app.get('/topic/username')
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(cleanup_message(response.data)))

    def test_subscription_get_no_subscription(self):
        response = self.app.get('/topic/username')
        self.assertEqual(404, response.status_code)

    def test_subscription_post(self):
        response = self.app.post('/topic/username')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(cleanup_message(response.data)))

    def test_subscription_post_duplicate(self):
        self.app.post('/topic/username')
        response = self.app.post('/topic/username')
        self.assertEqual(201, response.status_code)
        self.assertEqual(0, len(cleanup_message(response.data)))

    def test_subscription_delete(self):
        self.app.post('/topic/username')
        response = self.app.delete('/topic/username')
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(cleanup_message(response.data)))

    def test_subscription_delete_no_subscription(self):
        response = self.app.delete('/topic/username')
        self.assertEqual(404, response.status_code)

    def test_subscription_delete_with_messages(self):
        self.app.post('/topic/username')
        self.app.post('/topic', data='message',
                      headers={"content-type": "text/plain"})
        response = self.app.delete('/topic/username')
        self.assertEqual(200, response.status_code)
        response = self.app.get('/topic/username')
        self.assertEqual(404, response.status_code)

    def test_message_post(self):
        self.app.post('/topic/username')
        response = self.app.post('/topic', data='message',
                                 headers={"content-type": "text/plain"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(cleanup_message(response.data)))

    def test_message_post_many(self):
        self.app.post('/topic/username')
        message = "message%s"
        for i in xrange(3):
            response = self.app.post('/topic', data=(message % str(i)),
                                     headers={"content-type": "text/plain"})
            self.assertEqual(200, response.status_code)
            self.assertEqual(0, len(cleanup_message(response.data)))
        for j in xrange(3):
            response = self.app.get('/topic/username')
            expected = message % str(j)
            self.assertEqual(expected, cleanup_message(response.data))

    def test_message_post_no_subscription(self):
        response = self.app.post('/topic', data='message',
                                 headers={"content-type": "text/plain"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(cleanup_message(response.data)))
