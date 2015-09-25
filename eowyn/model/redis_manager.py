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

from eowyn import exceptions as eowyn_exc
from eowyn.model import manager


class RedisManager(manager.Manager):
    """Redis backed implementation of a model manager

    Subscriptions are sets of usernames associated to topic keys.
    Messages are lists associated topic.username keys.
    Redis key/pairs are thread/process safe, so this manager can be
    used when running Eowyn under uwsgi. With a Redis cluster Eowyn
    may scale across multiple nodes.

    Empty keys in Redis are automatically wiped, so this manager does
    not need to cleanup empty topic subscriptions nor empty message queues.
    """

    def __init__(self, host='localhost', port=6379, db=0):
        # By default we use db 0. Test uses db 1.
        _pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.store = redis.StrictRedis(connection_pool=_pool)

    def _queue(self, topic, username):
        # Name of the key for the message queue in Redis
        return ".".join([topic, username])

    def create_subscription(self, topic, username):
        super(RedisManager, self).create_subscription(topic, username)
        subscribers = self.store.smembers(topic)
        if subscribers and username in subscribers:
            raise eowyn_exc.SubscriptionAlreadyExistsException(
                topic=topic, username=username)
        self.store.sadd(topic, username)
        return topic

    def delete_subscription(self, topic, username):
        super(RedisManager, self).delete_subscription(topic, username)
        subscribers = self.store.smembers(topic)
        if username not in subscribers:
            raise eowyn_exc.SubscriptionNotFoundException(
                topic=topic, username=username)
        self.store.srem(topic, username)
        # Drop the corresponding message queue if it exists
        if self.store.exists(self._queue(topic, username)):
            self.store.delete(self._queue(topic, username))
        return topic

    def publish_message(self, topic, message):
        super(RedisManager, self).publish_message(topic, message)
        if topic in self.store:
            for username in self.store.smembers(topic):
                self.store.lpush(self._queue(topic, username), message)
        else:
            raise eowyn_exc.TopicNotFoundException(topic=topic)

    def pop_message(self, topic, username):
        super(RedisManager, self).pop_message(topic, username)
        if topic in self.store and username in self.store.smembers(topic):
            message = self.store.rpop(self._queue(topic, username))
            if not message:
                raise eowyn_exc.NoMessageFoundException(
                    topic=topic, username=username)
            else:
                return message
        else:
            raise eowyn_exc.SubscriptionNotFoundException(
                topic=topic, username=username)
