from typing import List, Any

from pydantic import HttpUrl

from ..config import AWS_REGION, AWS_DYNAMO_ENDPOINT
from ..cascade_types import FLAG_VALUE_TYPE
from .base import DynamoBaseModel


class Subscription(DynamoBaseModel):
    subscription_key: str
    flags: List[str]
    notification_key: HttpUrl

    class Config(DynamoBaseModel.Config):
        title = 'Subscription'
        hash_key = 'subscription_key'
        read = 1
        write = 1
        resource_kwargs = {
            'region_name': AWS_REGION,
            'endpoint_url': AWS_DYNAMO_ENDPOINT
        }

        @staticmethod
        def schema_extra(schema):
            # We remove the revision property from the schema because it is only used internally.
            schema['properties'].pop('revision')


def upsert(subscription: Subscription) -> Subscription:
    subscription.save()
    return subscription
