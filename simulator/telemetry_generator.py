
import random

from simulator.devices.device import DeviceStatus
from topology.link import LinkStatus
from network_collector.metrics import DeviceMetrics, LinkMetrics


class TelemetryGenerator:

    def __init__(self, network, seed=None):
        self.network = network
        self.random = random.Random(seed)

    def generate_device_metrics(self, device):

        return DeviceMetrics(
            device_id=device.device_id,
            cpu_percent=round(
                self.random.uniform(10, 65), 2
            ),
            memory_percent=round(
                self.random.uniform(20, 75), 2
            )
        )

    def generate_link_metrics(self, link):

        return LinkMetrics(
            link_id=link.link_id,
            latency_ms=round(
                self.random.uniform(1, 20), 2
            ),
            packet_loss_percent=round(
                self.random.uniform(0, 1), 2
            ),
            bandwidth_utilization_percent=round(
                self.random.uniform(10, 70), 2
            )
        )

    def collect_snapshot(self):

        device_metrics = []
        link_metrics = []

        # Collect metrics from operational devices
        for device in self.network.devices.values():

            if device.status == DeviceStatus.UP:
                device_metrics.append(
                    self.generate_device_metrics(device)
                )

        # Collect metrics from active links
        for link in self.network.links.values():

            source = self.network.devices[link.source_device_id]
            target = self.network.devices[link.target_device_id]

            if (
                link.status == LinkStatus.UP
                and source.status == DeviceStatus.UP
                and target.status == DeviceStatus.UP
            ):
                link_metrics.append(
                    self.generate_link_metrics(link)
                )

        return {
            "devices": device_metrics,
            "links": link_metrics
        }
