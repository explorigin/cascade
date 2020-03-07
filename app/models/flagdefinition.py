from typing import Literal
from uuid import UUID, uuid4

from pydantic import validator, BaseModel

from ..cascade_types import FLAG_VALUE_TYPE, FLAG_REVISIONED_VALUE_TYPE

SUPPORTED_DATATYPES = Literal['bool', 'str', 'int', 'float', 'datetime']


class FlagDefinition(BaseModel):
    key: str
    name: str
    description: str = ''
    datatype: SUPPORTED_DATATYPES
    default_value: FLAG_VALUE_TYPE

    @validator('default_value')
    def default_value_as_datatype(cls, v, values):
        type_name = values['datatype']
        typ = eval(type_name)
        if not isinstance(v, typ):
            try:
                return typ(v)
            except (TypeError, ValueError):
                raise ValueError(f'Cannot convert "{v}" into {type_name}.')
        return v


def get(project_key: str, flag_key: str) -> FlagDefinition:
    return FlagDefinition(key='karate',
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
