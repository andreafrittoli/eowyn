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

import abc
import collections
import exceptions
import six

from eowyn import exceptions as eowyn_exc


@six.add_metaclass(abc.ABCMeta)
class Manager(object):
    """Manager of subscription and messages

    Defines the API to manage subscriptions and messages.
    Defines data validation rules, which may be overwritten by specific
    manager implementations.
    """

    @abc.abstractmethod
    def create_subscription(self, topic, username):
        """Subscribe a user to a topic

        :param topic: topic to subscribe to
        :param username: username subscribing to the topic
        :returns: the topic for which a subscription was created
        :raises: eowyn_exc.SubscriptionAlreadyExistsException
        :raises: eowyn_exc.InvalidDataException
        """
        self.validate_topic(topic)
        self.validate_username(username)

    @abc.abstractmethod
    def delete_subscription(self, topic, username):
        """Unsubscribes a user from a topic

        :param topic: topic to un-subscribe from
        :param username: username un-subscribing from the topic
        :returns: the topic for which a subscription was deleted
        :raises: eowyn_exc.SubscriptionNotFoundException
        :raises: eowyn_exc.InvalidDataException
        """
        self.validate_topic(topic)
        self.validate_username(username)

    @abc.abstractmethod
    def publish_message(self, topic, message):
        """Publish a message to the subscribers of the topic

        :param topic: topic to publish to
        :param message: message to publish to the topic
        :returns: the published message
        :raises: eowyn_exc.TopicNotFoundException
        :raises: eowyn_exc.InvalidDataException
        """
        self.validate_topic(topic)
        self.validate_message(message)

    @abc.abstractmethod
    def pop_message(self, topic, username):
        """Pops the next message from a topic for the specific subscriber

        :param topic: topic to inspect
        :param username: get the next message on the topic for username
        :returns: the message
        :raises: eowyn_exc.SubscriptionNotFoundException
        :raises: eowyn_exc.NoMessageFoundException
        :raises: eowyn_exc.InvalidDataException
        """
        self.validate_topic(topic)
        self.validate_username(username)

    def validate_topic(self, topic):
        if topic is None:
            raise eowyn_exc.InvalidDataException(key='topic', value='None')

    def validate_username(self, username):
        if username is None:
            raise eowyn_exc.InvalidDataException(key='username', value='None')

    def validate_message(self, message):
        if message is None:
            raise eowyn_exc.InvalidDataException(key='message', value='None')


class SimpleManager(Manager):
    """Simple implementation of a model manager

    Subscriptions and messages are held in memory, as part of the manager
    itself. Subscriptions and messages are lost upon service restart.
    """

    def __init__(self):
        self.subscriptions = {}

    def create_subscription(self, topic, username):
        super(SimpleManager, self).create_subscription(topic, username)
        if self.subscriptions.get(topic, None) is None:
            self.subscriptions[topic] = {}
        elif username in self.subscriptions[topic]:
            raise eowyn_exc.SubscriptionAlreadyExistsException(
                topic=topic, username=username)
        _message_queue = collections.deque()
        self.subscriptions[topic][username] = _message_queue
        return topic

    def delete_subscription(self, topic, username):
        super(SimpleManager, self).delete_subscription(topic, username)
        if (self.subscriptions.get(topic, None) is None or username not in
                self.subscriptions[topic]):
            raise eowyn_exc.SubscriptionNotFoundException(
                topic=topic, username=username)
        del self.subscriptions[topic][username]
        # If the subscription was the last one, drop the topic
        if not self.subscriptions[topic]:
            del self.subscriptions[topic]
        return topic

    def publish_message(self, topic, message):
        super(SimpleManager, self).publish_message(topic, message)
        if topic in self.subscriptions.keys():
            for username in self.subscriptions[topic].keys():
                self.subscriptions[topic][username].appendleft(message)
        else:
            raise eowyn_exc.TopicNotFoundException(topic=topic)

    def pop_message(self, topic, username):
        super(SimpleManager, self).pop_message(topic, username)
        if topic in self.subscriptions.keys():
            if username in self.subscriptions[topic].keys():
                try:
                    return self.subscriptions[topic][username].pop()
                except exceptions.IndexError:
                    raise eowyn_exc.NoMessageFoundException(
                        topic=topic, username=username)
        else:
            raise eowyn_exc.SubscriptionNotFoundException(
                topic=topic, username=username)

classes = ['SimpleManager', 'RedisManager']


def get_manager(name='SimpleManager'):
    if name in classes:
        klass = globals().get(name, None)
        if klass is not None:
            return klass()
    else:
        raise eowyn_exc.InvalidManager(manager=name)
