from pydantic import validator, BaseModel

from ..cascade_types import FLAG_VALUE_TYPE, FLAG_VALUE_TYPE_NAMES, convert


class FlagDefinition(BaseModel):
    key: str
    name: str
    description: str = ''
    datatype: FLAG_VALUE_TYPE_NAMES
    default_value: FLAG_VALUE_TYPE

    @validator('default_value')
    def default_value_as_datatype(cls, value, values, config, field):
        try:
            type_name = values['datatype']
        except KeyError:
            raise ValueError('Datatype missing')

        try:
            return convert(value, type_name)
        except (TypeError, ValueError):
            raise ValueError(f'Cannot convert "{value}" into {type_name}.')
