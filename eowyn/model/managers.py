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
from eowyn.model import manager
from eowyn.model import redis_manager

classes = {'simple': manager.SimpleManager,
           'redis': redis_manager.RedisManager}


def get_manager(name='redis', **kwargs):
    # Defaults to `redis` as manager type. `simple` is only used for
    # testing purposes
    if name in classes.keys():
        return classes[name](**kwargs)
    else:
        raise eowyn_exc.InvalidManager(manager=name)
