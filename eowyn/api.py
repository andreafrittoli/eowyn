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


import ConfigParser
import flask
from flask import request
import flask_restful
import functools
import sys

import eowyn.exceptions as eowyn_exc
from eowyn.model import managers

app = flask.Flask(__name__)
api = flask_restful.Api(app)

manager = None


def handle_validate(f):
    """A decorator to apply handle data validation errors"""

    @functools.wraps(f)
    def wrapper(self, *func_args, **func_kwargs):
        try:
            return f(self, *func_args, **func_kwargs)
        except eowyn_exc.InvalidDataException as ida:
            flask_restful.abort(400, message=str(ida))
    return wrapper


class Subscription(flask_restful.Resource):

    @handle_validate
    def get(self, topic, username):
        # Get next message on a topic
        try:
            message = manager.pop_message(topic=topic, username=username)
            return message, 200
        except eowyn_exc.NoMessageFoundException:
            # If no message is found simply return 204
            return '', 204
        except eowyn_exc.SubscriptionNotFoundException as snfe:
            flask_restful.abort(404, message=str(snfe))

    @handle_validate
    def post(self, topic, username):
        # Subscribe to a topic
        try:
            manager.create_subscription(topic=topic, username=username)
            return '', 200
        except eowyn_exc.SubscriptionAlreadyExistsException:
            # NOTE(andreaf) This is not specified, but it seemed a
            # reasonable code to return in this case
            return '', 201

    @handle_validate
    def delete(self, topic, username):
        # Unsubscribe from a topic
        try:
            manager.delete_subscription(topic=topic, username=username)
            return '', 200
        except eowyn_exc.SubscriptionNotFoundException as snfe:
            flask_restful.abort(404, message=str(snfe))


class Message(flask_restful.Resource):

    @handle_validate
    def post(self, topic):
        # Post a message to a topic
        # There's no content type set for messages, they're plain text.
        # Because of that we need to extract the text from the
        # ImmutableMultiDIct returned by flask
        # message = request.form.keys()[0]
        message = request.data
        try:
            manager.publish_message(topic, message)
        except eowyn_exc.TopicNotFoundException:
            # NOTE(andreaf) When no topic is not found it means no subscription
            # exists so the message is discarded right away. We still need to
            # capture this exception, and do nothing for now. We may have
            # logging or reporting logic in future here.
            pass
        return '', 200


# Handle Subscriber API (subscribe, un-subscribe and get message)
api.add_resource(Subscription, '/<string:topic>/<string:username>')

# Handle Publisher API (post message)
api.add_resource(Message, '/<string:topic>')


def main():
    config = ConfigParser.ConfigParser()
    try:
        # Read config file as first command line parameter
        config_file = sys.argv[1]
        config.read(config_file)
        # Use the configured manager
        manager_type = config.get('default', 'manager')
        manager_configs = config.items(manager_type)
        # In case of duplicated configs, the last one wins
        manager_configs = {k: v for (k, v) in manager_configs}
        # Other configs
        debug = config.get('default', 'debug')
    except IndexError:
        # Or else use defaults
        debug = False
        manager_type = 'redis'
        manager_configs = {'host': 'localhost', 'port': 6379}
    global manager
    manager = managers.get_manager(manager_type, **manager_configs)
    app.run(debug=debug)

if __name__ == '__main__':
    main()
