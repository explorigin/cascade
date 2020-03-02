from uuid import UUID, uuid4

from pydantic import BaseModel

from ..types import FLAG_VALUE_TYPE, FLAG_REVISIONED_VALUE_TYPE


class Flag(BaseModel):
    key: str
    name: str
    description: str = ''
    datatype: str
    default_value: FLAG_VALUE_TYPE


def get(project_key: str, flag_key: str) -> Flag:
    return Flag(key='karate',
                name='Enable Japanese translations',
                datatype='bool',
                default_value=False)


def get_value(project_key: str, environment_key: str, flag_key: str) -> FLAG_REVISIONED_VALUE_TYPE:
    return True, uuid4()


def set_value(project_key: str,
              environment_key: str,
              flag_key: str,
              value: FLAG_VALUE_TYPE,
              revision: UUID = None) -> FLAG_REVISIONED_VALUE_TYPE:
    return value, uuid4()
