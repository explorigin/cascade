from typing import List

from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocket, WebSocketDisconnect
from boto3.dynamodb.conditions import Attr

from ..config import AWS_REGION, AWS_DYNAMO_ENDPOINT
from .base import UnversionedBaseModel
from ..models.project import get as get_project


class Subscription(UnversionedBaseModel):
    project_key: str
    environment_key: str
    flags: List[str]
    key: str

    class Config(UnversionedBaseModel.Config):
        title = 'Subscription'
        hash_key = 'key'
        read = 1
        write = 1
        resource_kwargs = {
            'region_name': AWS_REGION,
            'endpoint_url': AWS_DYNAMO_ENDPOINT
        }


class Notifier:
    def __init__(self, subscription_key: str):
        self.subscription_key = subscription_key
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self.notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        try:
            while True:
                await websocket.receive_json()
                await websocket.send_json({})
        except WebSocketDisconnect:
            self.remove(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)
        del _notifier_map[self.subscription_key]

    async def notify(self, data):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_json(data)
            living_connections.append(websocket)
        self.connections = living_connections


_notifier_map = {}


def get_notifier(subscription_key: str):
    Subscription.get(subscription_key)  # Eventually this will check permissions

    if subscription_key not in _notifier_map:
        _notifier_map[subscription_key] = Notifier(subscription_key)
    return _notifier_map[subscription_key]


def upsert(project: str,
           environment: str,
           flags: List[str]) -> Subscription:

    get_project(project, environment, flags)

    subscription = Subscription(
        project_key=project,
        environment_key=environment,
        flags=flags,
        key=str(uuid4()),
    )

    subscription.save()
    return subscription


async def notify(project_key: str, environment_key: str, flag_key: str, value):
    notifiers = {
        _notifier_map.get(subscription.key)
        for subscription in Subscription.query(
            Attr('project_key').eq(project_key)
            and Attr('environment_key').eq(environment_key)
            and Attr('flags').contains(flag_key)
        )
        if subscription.key in _notifier_map  # only if it exists
    }
    for n in notifiers:
        await n.notify({
            "project": project_key,
            "environment": environment_key,
            "flags": {
                flag_key: jsonable_encoder(value, exclude={'key', 'datatype'})
            }
        })
