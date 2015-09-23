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

The implementation provided here is an in-memory manager, where all objects 
are simply stored in memory. The in-memory manager does not support
horizontal scalability, and does not persist subscription across restarts.
This implementation is useful for development and for testing purposed, but 
it's not meant for production use.

Different implementation shall provide persistence of subscriptions across 
across restarts - which is not explicit requirement, but which seems a 
reasonable requirement. 

Horizontal capability can be achieved by running multiple instances of Eowyn
under a (stateless) load balancer. Multiple instance will then require 
concurrent access to subscriptions and messages. A DB or MQ backed 
implementation of the manager could support this kind of deployment 
architecture.