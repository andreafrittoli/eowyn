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

import flask
from flask import request
import flask_restful
import functools

import eowyn.exceptions as eowyn_exc
from model import manager

app = flask.Flask(__name__)
api = flask_restful.Api(app)

manager = manager.get_manager()


def handle_validate():
    """A decorator to apply handle data validation errors"""
    def decorator(f):

        @functools.wraps(f)
        def wrapper(self, *func_args, **func_kwargs):
            try:
                return f(self, *func_args, **func_kwargs)
            except eowyn_exc.InvalidDataException as ida:
                flask_restful.abort(400, str(ida))
        return wrapper
    return decorator


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
            flask_restful.abort(404, str(snfe))

    @handle_validate
    def post(self, topic, username):
        # Subscribe to a topic
        try:
            manager.create_subscriptions(topic=topic, username=username)
            return '', 200
        except eowyn_exc.SubscriptionAlreadyExistsException:
            # NOTE(andreaf) This is not specified, but it seemed a
            # reasonable code to return in this case
            return '', 201

    @handle_validate
    def delete(self, topic, username):
        # Unsubscribe from a topic
        try:
            manager.delete_subscriptions(topic=topic, username=username)
            return '', 200
        except eowyn_exc.SubscriptionNotFoundException as snfe:
            flask_restful.abort(404, str(snfe))


class Message(flask_restful.Resource):

    @handle_validate
    def post(self, topic):
        # Post a message to a topic
        # There's no content type set for messages, they're plain text.
        # Because of that we need to extract the text from the
        # ImmutableMultiDIct returned by flask
        message = request.form.keys()[0]
        try:
            manager.publish_messages(topic, message)
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

if __name__ == '__main__':
    app.run()
