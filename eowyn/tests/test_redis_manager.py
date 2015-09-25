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

import redis
import testtools

from eowyn.model import redis_manager
from eowyn.tests import test_simple_manager


class TestRedisManager(test_simple_manager.TestSimpleManager):

    def setUp(self):
        super(TestRedisManager, self).setUp()
        # Test require a local redis server running on the standard port
        # We use db 1 just in case the local db 0 is used for real data
        self.mgr = redis_manager.RedisManager(db=1)
        self.data = self.mgr.store
        # Connection is not actually attempted until a command is executed
        # Skip tests if the DB is not available
        try:
            self.data.flushdb()
        except redis.exceptions.ConnectionError as ce:
            msg = "Redis server not available: %s" % str(ce)
            raise testtools.TestCase.skipException(msg)

    def tearDown(self):
        super(TestRedisManager, self).tearDown()
        # Flushing before and after tests is a bit redundant, however
        # flushing it's cheap, and it avoids leaving stuff around after
        # the last tests run.
        self.data.flushdb()

    def get_queue(self, topic, username):
        qname = self.mgr._queue(topic, username)
        qlength = self.data.llen(qname)
        return self.data.lrange(qname, 0, qlength)

    def test_create_subscription(self):
        self.mgr.create_subscription('topic', 'username')
        self.assertIn('topic', self.data.keys('*'))
        self.assertIn('username', self.data.smembers('topic'))
        self.assertNotIn(self.mgr._queue('topic', 'username'),
                         self.data.keys('*'))

    def test_delete_subscription_single(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.delete_subscription('topic', 'username')
        self.assertNotIn('topic', self.data.keys('*'))

    def test_delete_subscription_multiple(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.create_subscription('topic', 'username2')
        self.mgr.delete_subscription('topic', 'username')
        self.assertIn('topic', self.data.keys('*'))
        self.assertNotIn('username', self.data.smembers('topic'))
        self.assertIn('username2', self.data.smembers('topic'))

    def test_publish_message(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.publish_message('topic', 'message')
        self.assertEqual(1,
                         self.get_queue('topic', 'username').count('message'))

    def test_publish_messages(self):
        self.mgr.create_subscription('topic', 'username')
        self.mgr.publish_message('topic', 'message')
        self.mgr.publish_message('topic', 'message2')
        self.assertEqual(1,
                         self.get_queue('topic', 'username').count('message'))
        self.assertEqual('message',
                         self.data.rpop(self.mgr._queue('topic', 'username')))

