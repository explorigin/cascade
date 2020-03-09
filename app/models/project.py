from typing import Dict

from .base import DynamoBaseModel
from ..config import AWS_DYNAMO_ENDPOINT, AWS_REGION
from .environment import Environment
from .flagdefinition import FlagDefinition


class Project(DynamoBaseModel):
    key: str
    name: str
    description: str = ''
    environments: Dict[str, Environment]
    flags: Dict[str, FlagDefinition]

    class Config(DynamoBaseModel.Config):
        title = 'Project'
        hash_key = 'key'
        read = 1
        write = 1
        resource_kwargs = {
            'region_name': AWS_REGION,
            'endpoint_url': AWS_DYNAMO_ENDPOINT
        }


def get(project_key: str) -> Project:
    return Project.get(project_key)


def upsert(project: Project) -> Project:
    project.save()
    return project
