
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import isfinite


@dataclass(frozen=True)
class DeviceMetrics:
    device_id: str
    cpu_percent: float
    memory_percent: float

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self):

        if not self.device_id.strip():
            raise ValueError("Device ID cannot be empty")

        if not isfinite(self.cpu_percent) or not 0 <= self.cpu_percent <= 100:
            raise ValueError("CPU must be between 0 and 100")

        if not isfinite(self.memory_percent) or not 0 <= self.memory_percent <= 100:
            raise ValueError("Memory must be between 0 and 100")

        if self.timestamp.tzinfo is None:
            raise ValueError("Timestamp must include timezone information")


@dataclass(frozen=True)
class LinkMetrics:
    link_id: str
    latency_ms: float
    packet_loss_percent: float
    bandwidth_utilization_percent: float

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self):

        if not self.link_id.strip():
            raise ValueError("Link ID cannot be empty")

        if not isfinite(self.latency_ms) or self.latency_ms < 0:
            raise ValueError("Latency cannot be negative")

        if not isfinite(self.packet_loss_percent) or not 0 <= self.packet_loss_percent <= 100:
            raise ValueError("Packet loss must be between 0 and 100")

        if not isfinite(self.bandwidth_utilization_percent) or not 0 <= self.bandwidth_utilization_percent <= 100:
            raise ValueError("Bandwidth utilization must be between 0 and 100")

        if self.timestamp.tzinfo is None:
            raise ValueError("Timestamp must include timezone information")
