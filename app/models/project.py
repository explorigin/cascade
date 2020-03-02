from typing import Dict

from pydantic import BaseModel

from .environment import Environment
from .flag import Flag


class Project(BaseModel):
    key: str
    name: str
    description: str = ''
    environments: Dict[str, Environment]
    flags: Dict[str, Flag]


def upsert_flag(project_id: str, flag: Flag) -> Flag:
    pass


def upsert_environment(project_id: str, env: Environment) -> Environment:
    pass


def get(project_key: str) -> Project:
    return Project(
        key=project_key,
        name='Cascade Dogfood',
        description='Cascade dogfooding itself',
        environments=dict(
            staging=Environment(
                name='staging',
                description='Staging Environment for new Features'
            ),
            production=Environment(
                name='production',
                description='Production'
            )
        ),
        flags=dict(
            supported_languages=Flag(
                key='supported_languages',
                name='Supported Languages',
                description='UI translations available',
                data_type='[str]',
                default_value='["en-US"]'
            )
        )
    )


def get_flags(project_id: str, environment_id: str):
    pass


def set_value():
    pass


def upsert():
    pass
