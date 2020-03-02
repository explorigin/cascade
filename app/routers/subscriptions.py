from fastapi import APIRouter

from ..models.subscription import Subscription

router = APIRouter()
TAGS = ["Subscriptions"]


@router.post("/{project}/{environment}", tags=TAGS)
async def subscribe(project: str, environment: str) -> Subscription:
    pass
