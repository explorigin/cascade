from uuid import UUID, uuid4

from pydantic import validator, BaseModel

from ..cascade_types import FLAG_VALUE_TYPE, FLAG_REVISIONED_VALUE_TYPE, FLAG_VALUE_TYPE_NAMES


class FlagDefinition(BaseModel):
    key: str
    name: str
    description: str = ''
    datatype: FLAG_VALUE_TYPE_NAMES
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
