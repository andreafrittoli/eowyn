# Design and Future Developments

Eowyn is designed as a horizontally scalable HTTP-based subscribe/publish
service implementation.

It's developed in pyhton. Development is test oriented, with unit test
implemented for all modules, as well as pep8 checks.

To ensure that the code is production quality:
- pep8 checks are executed against the code
- unit tests are provided for all modules, including the API
- all error code paths (and not only) are handled via custom exceptions
- the server is stateless and can scale horizontally, which ensures fault
  tolerance, and possibility to scale-out dynamically when under high load
  
Eowyn is easy install and configure. In can be installed in a python
virtual environment, and it's completely stateless, making it easy to update
on a running system. Redis does not use a fixed schema, so there is no
requirement for schema updates either. However a strategy must be designed to
support rolling upgrade and thus multiple versions of the data structures
co-existing in the same Redis DB.

There's more that could be done to ensure the quality of the software:
- HTTP API driven tests with random data injection
- Parallel API driven test, with concurrent test drivers.
- Load and long running tests to ensure there are no memory leaks
- High availability and fault tolerance tests

Feature-wise there are a few things that were not developed / configured due
to lack of time:
- logging must be setup before the service can be used in production
- monitoring can be achieved by standard tools, by verifying the availability
  of the process(es), and by probing the TCP port. A dedicated health-check
  topic may be used to validate service functionality - even though there is
  no mechanism to prevent public access to it
- a module matching the preferred deployment tools (ansible, puppet or else)
  must be developed to automatically deploy Eowyn in conjunction with uwsgi. 