from fastapi import APIRouter

from ..models.project import get, upsert, Project

router = APIRouter()
TAGS = ["Project"]


@router.get("/{project}", tags=TAGS)
async def get_project_details(project: str) -> Project:
    return get(project)


@router.put("/", tags=TAGS)
async def change_project_definition(project: Project) -> Project:
    return upsert(project)
