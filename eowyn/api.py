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
import flask_restful

from model import manager

app = flask.Flask(__name__)
api = flask_restful.Api(app)

manager = manager.get_manager()


class Subscription(flask_restful.Resource):

    def get(self, topic, username):
        # Get next message on a topic
        return {topic: username}

    def post(self, topic, username):
        # Subscribe to a topic
        return {topic: username}

    def delete(self, topic, username):
        # Unsubscribe from a topic
        return {topic: username}


class Message(flask_restful.Resource):

    def post(self, topic):
        # Post a message to a topic
        return {topic: 'foo'}


# Handle Subscriber API (subscribe, un-subscribe and get message)
api.add_resource(Subscription, '/<string:topic>/<string:username>')

# Handle Publisher API (post message)
api.add_resource(Message, '/<string:topic>')

if __name__ == '__main__':
    app.run()
