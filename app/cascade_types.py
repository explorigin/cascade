from datetime import datetime
from typing import Union, Literal, Dict
from uuid import UUID


FLAG_VALUE_TYPE_NAMES = Literal['bool', 'str', 'int', 'datetime']
FLAG_VALUE_TYPE = Union[bool, str, int, datetime]
FLAG_REVISIONED_VALUE_TYPE = Dict[Literal['value', 'revision'], Union[FLAG_VALUE_TYPE, UUID]]
