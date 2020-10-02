from typing import List

from uuid import uuid4

from .base import UnversionedBaseModel
from ..models.project import get as get_project


class Subscription(UnversionedBaseModel):
    project: str
    environment: str
    flags: List[str]
    key: str

    class Config(UnversionedBaseModel.Config):
        title = 'Subscription'
        hash_key = 'key'

    def get_data(self):
        # Need this here to avoid circular import.
        from .state import get_flag_data

        data = self.dict(exclude={'key', 'flags'})
        data['data'] = get_flag_data(
            self.project,
            self.environment,
            self.flags
        )
        return data


def upsert(project: str,
           environment: str,
           flags: List[str]) -> Subscription:

    # We don't technically need it, we're just making sure the subscription is valid.
    get_project(project, environment, flags)

    subscription = Subscription(
        project=project,
        environment=environment,
        flags=flags,
        key=str(uuid4()),
    )

    subscription.save()
    return subscription


