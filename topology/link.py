from dataclasses import dataclass
from enum import Enum


class LinkStatus(Enum):
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"


@dataclass
class NetworkLink:
    link_id: str
    source_device_id: str
    target_device_id: str
    bandwidth_mbps: float
    latency_ms: float = 1.0
    packet_loss_percent: float = 0.0
    status: LinkStatus = LinkStatus.UP

    def __post_init__(self):
        if not self.link_id.strip():
            raise ValueError("Link ID cannot be empty")

        if not self.source_device_id.strip():
            raise ValueError("Source device ID cannot be empty")

        if not self.target_device_id.strip():
            raise ValueError("Target device ID cannot be empty")

        if self.source_device_id == self.target_device_id:
            raise ValueError("A device cannot connect to itself")

        if self.bandwidth_mbps <= 0:
            raise ValueError("Bandwidth must be greater than zero")

        if self.latency_ms < 0:
            raise ValueError("Latency cannot be negative")

        if not 0 <= self.packet_loss_percent <= 100:
            raise ValueError("Packet loss must be between 0 and 100")
