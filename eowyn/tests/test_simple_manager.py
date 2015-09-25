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

import testtools

from eowyn import exceptions as eowyn_exc
from eowyn.model import manager
from eowyn.tests import base


class TestSimpleManager(base.TestCase):

    def setUp(self):
        super(TestSimpleManager, self).setUp()
        self.mgr = manager.SimpleManager()
        self.data = self.mgr.subscriptions

    def test_create_subscription(self):
        self.mgr.create_subscription('topic', 'username')
        self.assertIn('topic', self.data.keys())
        self.assertIn('username', self.data['topic'])
        with testtools.ExpectedException(IndexError):
            self.data['topic']['username'].pop()

    def test_create_subscription_exists(self):
        self.mgr.create_subscription('topic', 'username')
        with testtools.ExpectedException(
                eowyn_exc.SubscriptionAlreadyExistsException):
            self.mgr.create_subscription('topic', 'username')

    def test_create_subscription_invalid_data(self):
        for args in [(None, 'username'),
                     ('topic', None),
                     (None, None)]:
            with testtools.ExpectedException(
                    eowyn_exc.InvalidDataException):
                self.mgr.create_subscription(*args)

    def test_delete_subscription_single(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.delete_subscription('topic', 'username')
        self.assertNotIn('topic', self.data.keys())

    def test_delete_subscription_multiple(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.create_subscription('topic', 'username2')
        self.mgr.delete_subscription('topic', 'username')
        self.assertIn('topic', self.data.keys())
        self.assertNotIn('username', self.data['topic'].keys())
        self.assertIn('username2', self.data['topic'].keys())

    def test_delete_subscription_non_existent(self):
        self.mgr.create_subscription('topic', 'username')
        for args in [('topic2', 'username'),
                     ('topic', 'username2')]:
            with testtools.ExpectedException(
                    eowyn_exc.SubscriptionNotFoundException):
                self.mgr.delete_subscription(*args)

    def test_delete_subscription_invalid_data(self):
        for args in [(None, 'username'),
                     ('topic', None),
                     (None, None)]:
            with testtools.ExpectedException(
                    eowyn_exc.InvalidDataException):
                self.mgr.delete_subscription(*args)

    def test_publish_message(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.publish_message('topic', 'message')
        self.assertEqual(1, self.data['topic']['username'].count('message'))

    def test_publish_messages(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.publish_message('topic', 'message')
        self.mgr.publish_message('topic', 'message2')
        self.assertEqual(1, self.data['topic']['username'].count('message'))
        self.assertEqual('message', self.data['topic']['username'].pop())

    def test_publish_message_no_topic(self):
        with testtools.ExpectedException(eowyn_exc.TopicNotFoundException):
            self.mgr.publish_message('topic', 'message')

    def test_publish_message_invalid_data(self):
        for args in [(None, 'message'),
                     ('topic', None),
                     (None, None)]:
            with testtools.ExpectedException(
                    eowyn_exc.InvalidDataException):
                self.mgr.publish_message(*args)

    def test_pop_message(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.publish_message('topic', 'message')
        message = self.mgr.pop_message('topic', 'username')
        self.assertNotIn('message', self.data['topic']['username'])
        self.assertEqual('message', message)

    def test_pop_message_no_message(self):
        self.mgr.create_subscription('topic', 'username')
        with testtools.ExpectedException(eowyn_exc.NoMessageFoundException):
            self.mgr.pop_message('topic', 'username')

    def test_pop_message_no_subscription(self):
        self.mgr.create_subscription('topic', 'someone_else')
        with testtools.ExpectedException(
                eowyn_exc.SubscriptionNotFoundException):
            self.mgr.pop_message('topic', 'username')

    def test_pop_message_no_topic(self):
        with testtools.ExpectedException(
                eowyn_exc.SubscriptionNotFoundException):
            self.mgr.pop_message('topic', 'username')

    def test_pop_message_invalid_data(self):
        for args in [(None, 'username'),
                     ('topic', None),
                     (None, None)]:
            with testtools.ExpectedException(
                    eowyn_exc.InvalidDataException):
                self.mgr.pop_message(*args)
