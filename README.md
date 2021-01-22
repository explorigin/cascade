# Cascade

Cascade is a centralized feature flag manager to coordinate truth across multiple distinct projects.

Cascade clients will connect and subscribe to a preset collection of flags. If the flag is updated, cascade will propagate the change to all subscribed clients, tracing when a client has recognized the new flag. This way, new features can be switched on and off in seconds across any number of products.

## Concepts

### Projects

A project is a feature effort that can span multiple products. A good example of a project would be migrating between API versions for internal services.

### Environments

A project can have any number of environments assigned to it. The purpose of an environment is to provide different values for the same set of flags for different scenarios (e.g. you may want a feature enabled in on your testing servers but not in production yet).

### Flags

A flag is one datum that can be relevant across products or just one product that you want fine-control over. In the above API version situation a flag could be as simple as a boolean (`use_new_api`) or something more complicated (`authentication_api_url`).  


## Running the service

1. `docker-compose -f docker-compose.dynamo.yaml up -d`
2. `yarn install`
3. `yarn start`

NOTE: Replace `docker-compose.dynamo.yaml` with any of the other yaml files for different backend configurations.

Running this will give you an example app running at [http://localhost:8000](http://localhost:8000)

## Configuration

Cascade can be configured with a few environment variables:

- `cascade_backends` - Maps models to different backends. Each backend has its own set of environment variables for further configuration.
- `cascade_initialize` - Boolean - Should the backend be initialized (what this means is specific to the backend)

### Backends

You can mix multiple backends. by specifying different models in `cascade_backends`. Here's an example that uses SQLite for subscriptions and Dynamo for everything else:

```{"subscription": "app.backends.sqlite.Backend", "default": "app.backends.dynamodb.Backend"}```

Possible models are:
 - `subscription`
 - `project`
 - `state`

#### DynamoDB

Set `cascade_backends` to `{"default": "app.backends.dynamodb.Backend"}`. See `docker-compose.dynamo.yaml` as an example setup.

##### Environment Variables

 - `AWS_ACCESS_KEY_ID` - AWS API Key
 - `AWS_SECRET_ACCESS_KEY` - AWS API Secret
 - `DYNAMO_REGION` - AWS Region for dynamo tables
 - `DYNAMO_ENDPOINT` - Endpoint for dynamo server

#### SQLite

Set `cascade_backends` to `{"default": "app.backends.sqlite.Backend"}`. See `docker-compose.sqlite.yaml` as an example setup.

##### Environment Variables

 - `SQLITE_DB` - The database file to use
 
## Development

See the [development](./docs/development.md) documentation for details on setting up a development environment.
