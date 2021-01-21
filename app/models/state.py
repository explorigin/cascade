from typing import Optional, Dict, List

from uuid import UUID


from pydantic import validator
from .base import VersionedBaseModel
from .notification import notify
from .project import get as get_project
from ..cascade_types import FLAG_VALUE_TYPE, FLAG_VALUE_TYPE_NAMES, convert
from ..exceptions import DoesNotExist, RevisionMismatch


class State(VersionedBaseModel):
    key: str
    types: Dict[str, FLAG_VALUE_TYPE_NAMES]
    data: Dict[str, FLAG_VALUE_TYPE]

    @validator('data')
    def data_contains_the_right_type(cls, value, values, config, field) -> Dict[str, FLAG_VALUE_TYPE]:
        output = {}
        for flag_name, flag_type_name in values['types'].items():
            new_value = value[flag_name]

            try:
                output[flag_name] = convert(new_value, flag_type_name)
            except (TypeError, ValueError):
                raise ValueError(f'Cannot convert "{new_value}" in flag "{flag_name}" into {flag_type_name}.')

        return output

    class Config(VersionedBaseModel.Config):
        title = 'State'
        hash_key = 'key'


def _build_key(project_key: str, environment_key: str) -> str:
    return f'{project_key}_{environment_key}'


def _build_instance_from_default(project_key: str, environment_key: str):
    # Make sure the project exists
    project = get_project(project_key, environment_key)

    return State(
        key=_build_key(project_key, environment_key),
        data={k: v.default_value for k, v in project.flags.items()},
        types={k: v.datatype for k, v in project.flags.items()}
    )


def get(project_key: str,
        environment_key: str,
        create_from_default_if_missing: bool = True) -> State:
    value_key = _build_key(project_key, environment_key)

    try:
        return State.get(value_key)
    except DoesNotExist as e:
        if not create_from_default_if_missing:
            raise e
        state = _build_instance_from_default(project_key, environment_key)
        state.save()
        return state


async def set_value(project_key: str,
                    environment_key: str,
                    flag_key: str,
                    value: FLAG_VALUE_TYPE,
                    revision: Optional[UUID] = None) -> UUID:
    state_key = _build_key(project_key, environment_key)
    is_new = revision is None
    if is_new:
        try:
            # Just making sure it _doesn't_ exist
            State.get(state_key)
        except DoesNotExist:
            state = _build_instance_from_default(project_key, environment_key)
            state.data[flag_key] = value
            state.save()
            new_revision = state.revision
        else:
            raise RevisionMismatch('Provided revision is out of date' if revision else 'Must provide a revision')
    else:
        state = State.get(state_key)
        if state.revision != revision:
            raise RevisionMismatch('Provided revision is out of date')

        if state.data[flag_key] == value:
            # If the data is the same, short-circuit without having to hit the backend
            return is_new, state.revision

        state.data[flag_key] = value
        state.save()
        new_revision = state.revision

    if new_revision != revision:
        # Something was actually changed, so send a notification.
        await notify(project_key, environment_key, {[flag_key]: value})

    return is_new, new_revision


def get_flag_data(project_key: str, environment_key: str, flag_names: Optional[List[str]] = None):
    state = get(project_key, environment_key)
    flags = flag_names if flag_names is not None else state.types.keys()
    return {
        flag_name: dict(value=state.data[flag_name], datatype=state.types[flag_name])
        for flag_name in flags
    }
