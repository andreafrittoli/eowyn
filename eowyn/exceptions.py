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


class EowynException(Exception):

    message = 'Unknown Eowyn exception'

    def __init__(self, *args, **kwargs):
        super(EowynException, self).__init__()
        try:
            self._error_string = self.message % kwargs
        except Exception:
            # at least get the core message out if something happened
            self._error_string = self.message
        if len(args) > 0:
            # If there is a non-kwarg parameter, assume it's the error
            # message or reason description
            args = ["%s" % arg for arg in args]
            self._error_string = (self._error_string +
                                  "\nDetails: %s" % '\n'.join(args))


class InvalidManagerException(EowynException):
    message = 'Invalid manager %(manager)'


class SubscriptionAlreadyExistsException(EowynException):
    message = 'Subscription for %(username) already exists on %(topic)'


class SubscriptionNotFoundException(EowynException):
    message = 'Subscription for %(username) does not exists on %(topic)'


class TopicNotFoundException(EowynException):
    message = 'No subscription found for topic %(topic)'


class NoMessageFoundException(EowynException):
    message = 'No message found for username %(username) on topic %(topic)'

class InvalidDataException(EowynException):
    message = 'Invalid value %(value) for %(key)'
