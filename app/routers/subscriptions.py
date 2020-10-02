from typing import List

from fastapi import APIRouter, HTTPException
from starlette.websockets import WebSocket

from ..exceptions import DoesNotExist
from ..models.subscription import upsert
from ..models.notification import get_notifier

router = APIRouter()
TAGS = ["Subscriptions"]


@router.post("/{project}/{environment}", tags=TAGS, status_code=201)
async def subscribe(project: str, environment: str, flags: List[str]):
    try:
        subscription = upsert(project, environment, flags)
        return subscription.get_data()
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await get_notifier().connect(websocket)
