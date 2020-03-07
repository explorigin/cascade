from pydantic import BaseModel


class Environment(BaseModel):
    key: str
    description: str = ''
