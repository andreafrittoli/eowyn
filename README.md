# Eowyn

Eowyn is a simple implementation of a publish / subscribe server over HTTP.

Eowyn exposes and HTTP-based API that can be used to subscribe to specific
topics. When a client publishes messages to a specific topic, all subscribers
receive that message.

Once a message has been published:
- A message persist until all subscribers at the time of publishing have
  received it.
- A message is removed once all subscribers have received it

Eowyn is python based. It does not belong to the OpenStack ecosystem, however
it adopts coding style and testing tools from it.


## Install Eowyn  

Clone the repo:  

    git clone https://github.com/andreafrittoli/eowyn  

Install via pip:  

    cd eowyn 
    pip install .

## Test Eowyn

Tests can be executed via tox.
Syntax checks:

    tox -e pep8
    
Unit and functional tests:

    tox -e py27
    
## Configuring Eowyn

A configuration file may be used to configure Eowyn. 
A sample one is provided as part of Eowyn, under etc/api.sample.conf.

The default configuration uses a redis DB as backend. 
Make sure redis is running locally, or that host and port of the redis
DB are known.

Alternatively it is possible to run Eowyn with the `simple` manager.
The `simple` manager uses a python data structure to store subscriptions
and messages, and it's neither resilient to service restart nor
horizontally scalable, and it's only recommended for development / testing.

## Run Eowyn

Start Eowyn by running the flak app:

    eowyn-api [config-file]
    
If Eowyn is not installed, run the flask app from source:

    python eowyn/api.py [config-file]

## Using Eowyin

This is an example of how to interact with Eowyin via curl requests.

Create a subscription for `eowyn` to the `cats` topic:

    curl http://localhost:5000/cats/eowyn -X POST -v
    
Post a message to the `cats` topic:

    curl http://localhost:5000/cats -X POST -d 'http://cuteoverload.files.wordpress.com/2014/10/unnamed23.jpg?w=750&h=1000' -v -H 'content-type: plain/text'
    
Retrieve a message from the `cats` topic:

    curl http://localhost:5000/cats/eowyn -X GET -v

Delete a subscription for `eowyn` from the `cats` topic:

    curl http://localhost:5000/cats/andrea -X DELETE -v

## Deploying Eowyn

The recommended deployment stack for Eowyn is:

    Load balancer -> Nginx -> uwsgi -> Eowyn -> Redis (cluster) 

Eowyn can scale horizontally on a single server (e.g. via uwsgi) as well as
across multiple servers (e.g. via a load balanced Nginx).

The Redis backend ensures exclusive access to the keys in the store.

This configuration has not been tested E2E, because of lack of time.