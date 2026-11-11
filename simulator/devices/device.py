from dataclasses import dataclass
from enum import Enum
import ipaddress


class DeviceType(Enum):
    ROUTER = "router"
    SWITCH = "switch"
    SERVER = "server"


class DeviceStatus(Enum):
    UP = "up"
    DOWN = "down"
    DEGRADED = "degraded"


@dataclass
class Device:
    device_id: str
    hostname: str
    device_type: DeviceType
    management_ip: str

    status: DeviceStatus = DeviceStatus.UP
    cpu_percent: float = 0.0
    memory_percent: float = 0.0

    def __post_init__(self):
        if not self.device_id.strip():
            raise ValueError("Device ID cannot be empty")

        if not self.hostname.strip():
            raise ValueError("Hostname cannot be empty")

        try:
            ipaddress.ip_address(self.management_ip)
        except ValueError:
            raise ValueError(
                f"Invalid management IP: {self.management_ip}"
            )

        if not 0 <= self.cpu_percent <= 100:
            raise ValueError("CPU utilization must be between 0 and 100")

        if not 0 <= self.memory_percent <= 100:
            raise ValueError("Memory utilization must be between 0 and 100")
