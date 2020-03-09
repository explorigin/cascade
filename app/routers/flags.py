from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from ..cascade_types import FLAG_VALUE_TYPE, FLAG_REVISIONED_VALUE_TYPE
from ..models.flagvalue import get, set_value
from ..exceptions import DoesNotExist, RevisionMismatch

router = APIRouter()
TAGS = ["Flag"]


@router.get("/{project}/{environment}/{flag}", tags=TAGS)
async def get_flag_value(project: str,
                         environment: str,
                         flag: str) -> FLAG_REVISIONED_VALUE_TYPE:
    """Get the latest value for the given flag in the given environment and project."""

    try:
        return get(project, environment, flag).dict(exclude={'datatype', 'key'})
    except DoesNotExist as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{project}/{environment}/{flag}", tags=TAGS)
async def set_flag_value(project: str,
                         environment: str,
                         flag: str,
                         value: FLAG_VALUE_TYPE,
                         revision: UUID) -> FLAG_REVISIONED_VALUE_TYPE:
    """Update the value for the given flag in the given environment and project."""

    try:
        return set_value(project, environment, flag, value, revision)
    except DoesNotExist as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except RevisionMismatch as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
