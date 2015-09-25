# Eowyn Model Manager

The model manager provides a layer of abstraction between the resources in the
REST API and how they are managed, allowing for different implementations.

The model introduces managers for subscriptions and messages.

Subscriptions are identified by a topic and a username. Topics are ephemeral,
they exist only as long as a subscription for them.

Messages are added to topics, if a there is no subscription for a topic, the 
topic does not exists, and the message goes to /dev/null.
If there are subscriptions for a topic, the message exists as long either 
all subscribers have received it, or all related subscription have been 
cancelled.

Two implementations are provided here. 
Eowyn can be configured to use either implementation. 

The first one `SimpleManager` is an in-memory manager, where all objects are
stored in the memory space of the process running Eowyn. 
The in-memory manager does not support horizontal scalability, and does not
persist subscription across restarts.
This implementation is useful for development and for testing purposed, but 
it's not meant for production use.

The second one `RedisManager` stores objects in a Redis backend, and it
provides persistance of subscriptions and messages across restarts. This
is the manager enabled by default in Eowyn.

More implementations could be provided in-tree in future. There is no
plugin mechanism in place, but it could be easily added to allow for
3rd parties to maintain their backend plugin for Eowyn.