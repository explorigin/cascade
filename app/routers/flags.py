from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from ..cascade_types import FLAG_VALUE_TYPE, FLAG_REVISIONED_VALUE_TYPE
from ..models.flagdefinition import get, get_value, set_value, FlagDefinition
from ..models.project import upsert_flag
from ..exceptions import DoesNotExist

router = APIRouter()
TAGS = ["FlagDefinition"]


def set_flag_value_to_default(project_key, environment_key, flag_key) -> FLAG_REVISIONED_VALUE_TYPE:
    try:
        record = get(project_key, flag_key)
    except DoesNotExist:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'FlagDefinition "{flag_key}" does not exist.')
    return set_value(project_key, environment_key, flag_key, record.default_value)


@router.get("/{project}/{environment}/{flag}", tags=TAGS)
async def get_flag_value(project: str,
                         environment: str,
                         flag: str) -> FLAG_REVISIONED_VALUE_TYPE:
    """Get the latest value for the given flag in the given environment and project."""

    try:
        return get_value(project, environment, flag)
    except DoesNotExist:
        return set_flag_value_to_default(project, environment, flag)


@router.put("/{project}/flag", tags=TAGS)
async def change_flag_definition(project: str, flag: FlagDefinition) -> FlagDefinition:
    """Create or change the a flag definition in the given project."""

    return upsert_flag(project, flag)


@router.patch("/{project}/{environment}/{flag}", tags=TAGS)
async def set_flag_value(project: str,
                         environment: str,
                         flag: str,
                         value: FLAG_VALUE_TYPE,
                         revision: UUID) -> FLAG_REVISIONED_VALUE_TYPE:
    """Update the value for the given flag in the given environment and project."""

    try:
        record = get_value(project, environment, flag)
        if record.revision != revision:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=f'Revision does not match.')
        return set_value(project, environment, flag, value, revision)
    except DoesNotExist:
        return set_flag_value_to_default(project, environment, flag)
