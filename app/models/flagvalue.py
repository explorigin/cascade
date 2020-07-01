from typing import Optional

from uuid import UUID

from pydantic import validator
from .base import DynamoBaseModel
from ..config import AWS_DYNAMO_ENDPOINT, AWS_REGION
from ..cascade_types import FLAG_VALUE_TYPE, FLAG_VALUE_TYPE_NAMES
from ..exceptions import DoesNotExist, RevisionMismatch


class FlagValue(DynamoBaseModel):
    key: str
    datatype: FLAG_VALUE_TYPE_NAMES
    value: FLAG_VALUE_TYPE

    @validator('value')
    def default_value_as_datatype(cls, v, values) -> FLAG_VALUE_TYPE_NAMES:
        type_name = values['datatype']
        typ = eval(type_name)
        if not isinstance(v, typ):
            try:
                return typ(v)
            except (TypeError, ValueError):
                raise ValueError(f'Cannot convert "{v}" into {type_name}.')
        return v

    class Config(DynamoBaseModel.Config):
        title = 'FlagValue'
        hash_key = 'key'
        read = 1
        write = 1
        resource_kwargs = {
            'region_name': AWS_REGION,
            'endpoint_url': AWS_DYNAMO_ENDPOINT
        }


def _validate_flag_definition(project_key: str, environment_key: str, flag_definition_key: str):
    from .project import get as get_project

    project = get_project(project_key)
    if environment_key not in project.environments:
        raise DoesNotExist(f'Environment "{environment_key}" does not exist in project "{project_key}"')
    if flag_definition_key not in project.flags:
        raise DoesNotExist(f'Flag "{flag_definition_key}" does not exist in project "{project_key}"')

    return project

def _build_key(project_key: str, environment_key: str, flag_definition_key: str) -> str:
    _validate_flag_definition(project_key, environment_key, flag_definition_key)

    return f'{project_key}_{environment_key}_{flag_definition_key}'


def _build_instance_from_default(project_key: str, environment_key: str, flag_definition_key: str):
    project = _validate_flag_definition(project_key, environment_key, flag_definition_key)

    definition = project.flags[flag_definition_key]
    return FlagValue(
        key=_build_key(project_key, environment_key, flag_definition_key),
        datatype=definition.datatype,
        value=definition.default_value
    )


def get(project_key: str,
        environment_key: str,
        flag_key: str,
        create_from_default_if_missing: bool = True) -> (bool, FlagValue):
    value_key = _build_key(project_key, environment_key, flag_key)

    try:
        return FlagValue.get(value_key)
    except DoesNotExist as e:
        if not create_from_default_if_missing:
            raise e
        flag_value = _build_instance_from_default(project_key, environment_key, flag_key)
        flag_value.save()
        return flag_value


async def set_value(project_key: str,
                    environment_key: str,
                    flag_definition_key: str,
                    value: FLAG_VALUE_TYPE,
                    revision: Optional[UUID] = None) -> UUID:
    value_key = _build_key(project_key, environment_key, flag_definition_key)
    is_new = revision is None
    new_revision = None
    if is_new:
        try:
            FlagValue.get(value_key)
        except DoesNotExist:
            flag_value = _build_instance_from_default(project_key, environment_key, flag_definition_key)
            flag_value.value = value
            flag_value.save()
            new_revision = flag_value.revision
        else:
            raise RevisionMismatch('Provided revision is out of date' if revision else 'Must provide a revision')
    else:
        new_revision = FlagValue.update_value(
            value_key,
            'value',
            value,
            revision
        )

    return is_new, new_revision
