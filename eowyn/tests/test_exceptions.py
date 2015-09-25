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

from eowyn import exceptions as eowyn_exc
from eowyn.tests import base


class TestExceptions(base.TestCase):

    def test_eowyn_exception(self):
        exc = eowyn_exc.EowynException()
        self.assertIn('Unknown Eowyn exception', str(exc))

    def test_eowyn_exception_params(self):
        exc = eowyn_exc.EowynException('a', b='B')
        self.assertIn('Unknown Eowyn exception', str(exc))

    def test_invalid_manager_exception(self):
        exc = eowyn_exc.InvalidManagerException(manager='manager1')
        self.assertIn('manager1', str(exc))

    def test_invalid_manager_exception_invalid_param(self):
        exc = eowyn_exc.InvalidManagerException(foo='bar1')
        self.assertNotIn('bar1', str(exc))

    def test_subscription_already_exists_exception(self):
        exc = eowyn_exc.SubscriptionAlreadyExistsException(
            username='username1', topic='topic1')
        self.assertIn('username1', str(exc))
        self.assertIn('topic1', str(exc))

    def test_subscription_already_exists_exception_invalid_param(self):
        exc = eowyn_exc.SubscriptionAlreadyExistsException(foo='bar1')
        self.assertNotIn('bar1', str(exc))

    def test_subscription_not_found_exception(self):
        exc = eowyn_exc.SubscriptionNotFoundException(
            username='username1', topic='topic1')
        self.assertIn('username1', str(exc))
        self.assertIn('topic1', str(exc))

    def test_subscription_not_found_exception_invalid_param(self):
        exc = eowyn_exc.SubscriptionNotFoundException(foo='bar1')
        self.assertNotIn('bar1', str(exc))

    def test_topic_not_found_exception(self):
        exc = eowyn_exc.TopicNotFoundException(topic='topic1')
        self.assertIn('topic1', str(exc))

    def test_topic_not_found_exception_invalid_param(self):
        exc = eowyn_exc.TopicNotFoundException(foo='bar1')
        self.assertNotIn('bar1', str(exc))

    def test_no_message_found_exception(self):
        exc = eowyn_exc.NoMessageFoundException(
            username='username1', topic='topic1')
        self.assertIn('username1', str(exc))
        self.assertIn('topic1', str(exc))

    def test_no_message_found_exception_invalid_param(self):
        exc = eowyn_exc.NoMessageFoundException(foo='bar1')
        self.assertNotIn('bar1', str(exc))

    def test_invalid_data_exception(self):
        exc = eowyn_exc.InvalidDataException(key='key1', value='value1')
        self.assertIn('key1', str(exc))
        self.assertIn('value1', str(exc))

    def test_invalid_data_exception_invalid_param(self):
        exc = eowyn_exc.InvalidDataException(foo='bar1')
        self.assertNotIn('bar1', str(exc))

