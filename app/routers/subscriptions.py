from typing import List

from fastapi import APIRouter, HTTPException
from starlette.websockets import WebSocket

from ..exceptions import DoesNotExist
from ..models.subscription import upsert, get_notifier
from ..models.flagvalue import get

router = APIRouter()
TAGS = ["Subscriptions"]


@router.post("/{project}/{environment}/{subscription_name}", tags=TAGS)
async def subscribe(project: str, environment: str, flags: List[str]):
    try:
        subscription = upsert(project, environment, flags)
        data = subscription.dict()
        data['data'] = {
            flag_key: get(project, environment, flag_key).dict(exclude={'key'})
            for flag_key in subscription.flags
        }
        return data
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.websocket("/{subscription_key}/ws")
async def websocket_endpoint(subscription_key: str, websocket: WebSocket):
    try:
        notifier = get_notifier(subscription_key)
    except DoesNotExist:
        await websocket.close(code=404)
    else:
        await notifier.connect(websocket)
