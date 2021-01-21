# Local Development

If you want to debug in PyCharm:

1. Run the steps [Running the Service](./README.md#Running_the_service) steps.
2. `docker-compose -f docker-compose.dynamo.yaml stop cascade`
3. Start your `Debug` job in PyCharm.

## PyCharm Setup

Pycharm can help manage services with Docker Compose, but it is necessary for setting up a remote interpreter.

To setup a "Debug" job, create a Python script with the docker-compose remote interpreter. Use the following settings:
  - script: `[project root]/debug.py`
  - path mappings:
    - `[project root]` -> `/application`
