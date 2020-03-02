from fastapi import APIRouter

from ..models.environment import Environment
from ..models.project import upsert_environment

router = APIRouter()
TAGS = ["Environment"]


@router.put("/{project}/environment", tags=TAGS)
async def change_environment_definition(project: str, env: Environment) -> Environment:
    return upsert_environment(project, env)
