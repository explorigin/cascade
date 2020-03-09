from typing import Union, Literal
from datetime import datetime
from uuid import UUID


FLAG_VALUE_TYPE_NAMES = Literal['bool', 'str', 'int', 'datetime']
FLAG_VALUE_TYPE = Union[bool, str, int, datetime]
FLAG_REVISIONED_VALUE_TYPE = FLAG_VALUE_TYPE, UUID
UUID_STR = str
