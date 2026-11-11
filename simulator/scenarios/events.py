from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4


class EventType(Enum):
    DEVICE_DOWN = "device_down"
    DEVICE_UP = "device_up"


@dataclass
class NetworkEvent:
    event_id: str
    event_type: EventType
    device_id: str
    timestamp: datetime
    description: str


def create_event(
    event_type: EventType,
    device_id: str,
    description: str
) -> NetworkEvent:

    return NetworkEvent(
        event_id=str(uuid4()),
        event_type=event_type,
        device_id=device_id,
        timestamp=datetime.now(timezone.utc),
        description=description
    )
