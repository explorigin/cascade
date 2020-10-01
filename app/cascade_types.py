from distutils.util import strtobool
from datetime import datetime
from typing import Union, Literal, Dict
from uuid import UUID


FLAG_VALUE_TYPE_NAMES = Literal['bool', 'str', 'int', 'datetime']
FLAG_VALUE_TYPE = Union[bool, str, int, datetime]
FLAG_REVISIONED_VALUE_TYPE = Dict[Literal['value', 'revision'], Union[FLAG_VALUE_TYPE, UUID]]


def convert(value: FLAG_VALUE_TYPE, type_name: FLAG_VALUE_TYPE_NAMES):
    typ = eval(type_name)

    if isinstance(value, typ):
        return value

    if type_name == 'bool':
        return strtobool(value)

    return typ(value)
