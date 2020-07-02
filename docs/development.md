# Local Development

To just run the service:

1. `docker-compose build`
2. `docker-compose up -d`

NOTE: The `bootstrap` service merely creates dynamo tables if they don't
 exist and then exits. It is normal for it to not stay running.

If you want to debug in PyCharm:

3. `docker-compose stop cascade`
4. Start your `Debug` job in Python 

## PyCharm Setup

Pycharm can help manage services with Docker Compose, but it is necessary for
 setting up a remote interpreter.

To setup a "Debug" job, create a Python script with the docker-compose remote
 interpreter. Use the following settings:
  - script: `[project root]/debug.py`
  - path mappings:
    - `[project root]` -> `/application`
