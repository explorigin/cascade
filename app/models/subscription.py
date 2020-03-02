from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel

WEBHOOK = 'webhook'
POLL = 'poll'
WEBSOCKET = 'websocket'


class Subscription(BaseModel):
    type: str = WEBHOOK
    project_key: str
    environment_key: str
    flags: List[str]
    revision_timestamp: datetime
    poll_interval: Optional[timedelta]
    next_expected_poll: Optional[datetime]
