from fastapi import APIRouter

from ..models.subscription import Subscription, upsert

router = APIRouter()
TAGS = ["Subscriptions"]


@router.post("/", tags=TAGS)
async def subscribe(subscription: Subscription) -> Subscription:
    return upsert(subscription)
