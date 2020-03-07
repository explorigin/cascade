from typing import Dict

from .base import DynamoBaseModel
from ..config import AWS_DYNAMO_ENDPOINT, AWS_REGION
from .environment import Environment
from .flag import Flag


class Project(DynamoBaseModel):
    key: str
    name: str
    description: str = ''
    environments: Dict[str, Environment]
    flags: Dict[str, Flag]

    class Config(DynamoBaseModel.Config):
        title = 'Project'
        hash_key = 'key'
        read = 1
        write = 1
        resource_kwargs = {
            'region_name': AWS_REGION,
            'endpoint_url': AWS_DYNAMO_ENDPOINT
        }


def upsert_flag(project_id: str, flag: Flag) -> Flag:
    pass


def get(project_key: str) -> Project:
    return Project.get(project_key)


def upsert_environment(project_key: str, env: Environment) -> Environment:
    project = get(project_key)
    project.environments[env.key] = env
    project.save()
    return env


def get_flags(project_id: str, environment_id: str):
    pass


def set_value():
    pass


def upsert(project: Project):
    res = project.save()
    return res
