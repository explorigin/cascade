from fastapi import APIRouter, HTTPException

from ..exceptions import DoesNotExist, RevisionMismatch
from ..models.project import get, upsert, Project

router = APIRouter(routes='/project')
TAGS = ["Project"]


@router.get("/{project}", tags=TAGS)
async def get_project_details(project: str) -> Project:
    try:
        return get(project)
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/", tags=TAGS)
async def change_project_definition(project: Project) -> Project:
    try:
        upsert(project)
    except RevisionMismatch as e:
        raise HTTPException(status_code=409, detail=str(e))
    return project
