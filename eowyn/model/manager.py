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
import six


@six.add_metaclass(abc.ABCMeta)
class Subscription(object):
    """Controller of subscriptions.

    Defines the API to manage subscriptions.
    """

    @abc.abstractmethod
    def create(self, topic, username):
        """Subscribe a user to a topic"""
        pass

    @abc.abstractmethod
    def delete(self, topic, username):
        """Unsubscribes a user from a topic"""
        pass


@six.add_metaclass(abc.ABCMeta)
class Message(object):
    """Controller of messages.

    Defines the API to manage messages.
    """

    @abc.abstractmethod
    def publish(self, topic, message):
        """Publish a message to the subscribers of the topic"""
        pass

    @abc.abstractmethod
    def pop(self, topic, username):
        """Pops the next message from a topic for the specific subscriber"""
        pass
