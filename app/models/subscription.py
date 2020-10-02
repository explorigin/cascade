from typing import List

from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from rule_engine import Rule
from starlette.websockets import WebSocket, WebSocketDisconnect

from .base import UnversionedBaseModel
from .state import get_flag_data
from ..exceptions import DoesNotExist
from ..models.project import get as get_project
from ..cascade_types import FLAG_VALUE_TYPE


class Subscription(UnversionedBaseModel):
    project: str
    environment: str
    flags: List[str]
    key: str

    class Config(UnversionedBaseModel.Config):
        title = 'Subscription'
        hash_key = 'key'

    def get_data(self):
        data = self.dict(exclude={'key', 'flags'})
        data['data'] = get_flag_data(
            self.subscription.project,
            self.subscription.environment,
            self.subscription.flags
        )

class Notifier:
    def __init__(self):
        self.subscription = None
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
                data = await websocket.receive_json()
                if self.subscription is None:
                    try:
                        self.subscription = upsert(**data)
                    except DoesNotExist:
                        await self.remove(websocket, 4004)
                        return
                    _notifier_map[self.subscription.key] = self
                    _unknown_list.remove(self)
                    await websocket.send_json(self.subscription.get_data())
                else:
                    await self.remove(websocket, 4009)
        except WebSocketDisconnect:
            await self.remove(websocket)

    async def remove(self, websocket: WebSocket, code=1000):
        await websocket.close(code)
        self.connections.remove(websocket)
        try:
            _unknown_list.remove(self)
        except ValueError:
            pass
        try:
            del _notifier_map[self.subscription.key]
        except (KeyError, AttributeError):
            pass

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
_unknown_list = []


def get_notifier():
    notifier = Notifier()
    _unknown_list.append(notifier)
    return notifier


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


async def notify(project_key: str, environment_key: str, flag_key: str, value: FLAG_VALUE_TYPE):
    subscriptions = Subscription.query(
        Rule(f"project == '{project_key}' and environment == '{environment_key}' and '{flag_key}' in flags")
    )
    notifiers = {
        _notifier_map.get(subscription.key)
        for subscription in subscriptions
        if subscription.key in _notifier_map  # only if it exists
    }

    # Notify known subscriptions
    for n in notifiers:
        await n.notify({
            "project": project_key,
            "environment": environment_key,
            "data": {
                flag_key: jsonable_encoder({"value": value})
            }
        })

    # Clean up stale subscriptions
    for subscription in subscriptions:
        if subscription.key not in _notifier_map:
            Subscription.delete(subscription.key)
