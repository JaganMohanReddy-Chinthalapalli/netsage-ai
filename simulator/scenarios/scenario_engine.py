from simulator.devices.device import DeviceStatus
from simulator.scenarios.events import (
    EventType,
    NetworkEvent,
    create_event
)


class ScenarioEngine:

    def __init__(self, network):
        self.network = network
        self.events: list[NetworkEvent] = []

    def fail_device(self, device_id: str):

        if device_id not in self.network.devices:
            raise ValueError(f"Unknown device: {device_id}")

        device = self.network.devices[device_id]

        if device.status == DeviceStatus.DOWN:
            raise ValueError(f"{device_id} is already DOWN")

        device.status = DeviceStatus.DOWN

        event = create_event(
            EventType.DEVICE_DOWN,
            device_id,
            f"Device {device_id} went DOWN"
        )

        self.events.append(event)

        return event

    def recover_device(self, device_id: str):

        if device_id not in self.network.devices:
            raise ValueError(f"Unknown device: {device_id}")

        device = self.network.devices[device_id]

        if device.status == DeviceStatus.UP:
            raise ValueError(f"{device_id} is already UP")

        device.status = DeviceStatus.UP

        event = create_event(
            EventType.DEVICE_UP,
            device_id,
            f"Device {device_id} recovered and is UP"
        )

        self.events.append(event)

        return event

    def get_events(self):
        return list(self.events)
