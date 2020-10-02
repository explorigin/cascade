from typing import Optional

from uuid import UUID

from fastapi import APIRouter, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from ..cascade_types import FLAG_VALUE_TYPE, FLAG_REVISIONED_VALUE_TYPE
from ..models.state import get, set_value
from ..exceptions import DoesNotExist, RevisionMismatch

router = APIRouter()
TAGS = ["Flag"]


@router.get("/{project}/{environment}/{flag}", tags=TAGS)
async def get_flag_value(project: str,
                         environment: str,
                         flag: str) -> FLAG_REVISIONED_VALUE_TYPE:
    """Get the latest value for the given flag in the given environment and project."""

    try:
        state = get(project, environment)
        return dict(revision=state.revision, value=state.data[flag])
    except (DoesNotExist, KeyError) as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{project}/{environment}/{flag}", tags=TAGS, status_code=200)
async def set_flag_value(response: Response,
                         project: str,
                         environment: str,
                         flag: str,
                         value: FLAG_VALUE_TYPE,
                         revision: Optional[UUID] = None) -> UUID:
    """Update the value for the given flag in the given environment and project."""

    try:
        is_new, new_revision = await set_value(project, environment, flag, value, revision)
        if is_new:
            response.status_code = 201  # Value did not previously exist, created
        elif new_revision == revision:
            response.status_code = 204  # Value not changed
        return new_revision
    except DoesNotExist as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise RequestValidationError(e.raw_errors)
    except RevisionMismatch as e:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail=str(e))
