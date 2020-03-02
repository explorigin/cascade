# Cascade

Cascade is a centralized feature flag manager to coordinate truth across
multiple distinct projects.

Cascade clients will connect and subscribe to a preset collection of flags. If
the flag is updated, cascade will propagate the change to all clients, tracing
when a client has recognized the new flag. This way, new features can be
switched on and off in less than a second across any number of products.

## Projects

A project is a feature effort that can span multiple projects. A good example
of a project would be migrating between API versions for internal services.

## Environments

A project can have any number of environments assigned to it. The purpose of an
environment is to provide different values for the same set of flags for
different scenarios (e.g. you may want a feature enabled in on your testing
servers but not in production yet).

## Flags

A flag is one datum that can be relevant across projects or servers. In the
above API version situation a flag could be as simple as a boolean
 (`use_new_api`) or something more complicated (`authentication_api_url`).  


