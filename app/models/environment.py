from pydantic import BaseModel


class Environment(BaseModel):
    name: str
    description: str = ''

