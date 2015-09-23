# eowyn

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