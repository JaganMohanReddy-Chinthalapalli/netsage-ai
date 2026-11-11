from collections import deque

from simulator.devices.device import Device, DeviceStatus
from topology.link import NetworkLink, LinkStatus


class NetworkTopology:

    def __init__(self):
        self.devices = {}
        self.links = {}

    def add_device(self, device: Device):

        if device.device_id in self.devices:
            raise ValueError(
                f"Device already exists: {device.device_id}"
            )

        self.devices[device.device_id] = device

    def add_link(self, link: NetworkLink):

        if link.link_id in self.links:
            raise ValueError(
                f"Link already exists: {link.link_id}"
            )

        if link.source_device_id not in self.devices:
            raise ValueError("Source device does not exist")

        if link.target_device_id not in self.devices:
            raise ValueError("Target device does not exist")

        self.links[link.link_id] = link

    def get_neighbors(
        self,
        device_id: str,
        include_inactive: bool = False
    ):

        if device_id not in self.devices:
            raise ValueError(f"Unknown device: {device_id}")

        neighbors = []

        for link in self.links.values():

            if not include_inactive and link.status != LinkStatus.UP:
                continue

            if link.source_device_id == device_id:
                neighbors.append(
                    self.devices[link.target_device_id]
                )

            elif link.target_device_id == device_id:
                neighbors.append(
                    self.devices[link.source_device_id]
                )

        return neighbors

    def get_reachable_devices(self, start_device_id: str):

        if start_device_id not in self.devices:
            raise ValueError(
                f"Unknown starting device: {start_device_id}"
            )

        start_device = self.devices[start_device_id]

        if start_device.status != DeviceStatus.UP:
            return set()

        visited = set()
        queue = deque([start_device_id])

        while queue:

            current_id = queue.popleft()

            if current_id in visited:
                continue

            current_device = self.devices[current_id]

            if current_device.status != DeviceStatus.UP:
                continue

            visited.add(current_id)

            for neighbor in self.get_neighbors(current_id):

                if (
                    neighbor.status == DeviceStatus.UP
                    and neighbor.device_id not in visited
                ):
                    queue.append(neighbor.device_id)

        return visited

    def find_unreachable_devices(self, start_device_id: str):

        reachable = self.get_reachable_devices(start_device_id)

        unreachable = []

        for device in self.devices.values():

            if (
                device.status == DeviceStatus.UP
                and device.device_id not in reachable
            ):
                unreachable.append(device)

        return unreachable
