from typing import Dict, Optional, Union, List

from .base import VersionedBaseModel
from ..config import AWS_DYNAMO_ENDPOINT, AWS_REGION
from .environment import Environment
from .flagdefinition import FlagDefinition
from ..exceptions import DoesNotExist


class Project(VersionedBaseModel):
    key: str
    name: str
    description: str = ''
    environments: Dict[str, Environment]
    flags: Dict[str, FlagDefinition]

    class Config(VersionedBaseModel.Config):
        title = 'Project'
        hash_key = 'key'
        read = 1
        write = 1
        resource_kwargs = {
            'region_name': AWS_REGION,
            'endpoint_url': AWS_DYNAMO_ENDPOINT
        }


def get(project_key: str,
        environment_key: Optional[str] = None,
        flag_definition_key_or_list: Optional[Union[str, List[str]]] = None) -> Project:
    project = Project.get(project_key)

    if environment_key is not None and environment_key not in project.environments:
        raise DoesNotExist(f'Environment "{environment_key}" does not exist in project "{project_key}"')

    if flag_definition_key_or_list is None:
        return project

    requested_flag_set = (
        set(flag_definition_key_or_list)
        if isinstance(flag_definition_key_or_list, list)
        else set([flag_definition_key_or_list])
    )

    missing_flags = requested_flag_set.difference(set(project.flags.keys()))
    if missing_flags:
        raise DoesNotExist(f'Flag "{missing_flags.pop()}" does not exist in project "{project_key}"')

    return project


def upsert(project: Project) -> Project:
    project.save()
    return project
