from typing import List

from fastapi import APIRouter, HTTPException
from starlette.websockets import WebSocket

from ..exceptions import DoesNotExist
from ..models.subscription import upsert, get_notifier
from ..models.state import get

router = APIRouter()
TAGS = ["Subscriptions"]


@router.post("/{project}/{environment}", tags=TAGS, status_code=201)
async def subscribe(project: str, environment: str, flags: List[str]):
    try:
        subscription = upsert(project, environment, flags)
        data = subscription.dict()
        data['data'] = {
            flag_key: get(project, environment, flag_key).dict(exclude={'key', 'revision'})
            for flag_key in subscription.flags
        }
        return data
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await get_notifier().connect(websocket)
