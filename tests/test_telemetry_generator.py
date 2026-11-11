
from simulator.devices.device import (
    Device,
    DeviceType,
    DeviceStatus
)
from topology.link import NetworkLink
from topology.network_topology import NetworkTopology
from simulator.telemetry_generator import TelemetryGenerator


def main():

    # Build network
    network = NetworkTopology()

    devices = [
        Device("R1", "R1", DeviceType.ROUTER, "192.168.1.1"),
        Device("S1", "S1", DeviceType.SWITCH, "192.168.1.2"),
        Device("S2", "S2", DeviceType.SWITCH, "192.168.1.3"),
        Device("SRV1", "SRV1", DeviceType.SERVER, "192.168.1.10"),
        Device("SRV2", "SRV2", DeviceType.SERVER, "192.168.1.11"),
    ]

    for device in devices:
        network.add_device(device)

    links = [
        NetworkLink("L1", "R1", "S1", 1000),
        NetworkLink("L2", "S1", "S2", 1000),
        NetworkLink("L3", "S2", "SRV1", 1000),
        NetworkLink("L4", "S2", "SRV2", 1000),
    ]

    for link in links:
        network.add_link(link)

    # Initialize generator
    generator = TelemetryGenerator(network, seed=42)

    # Collect normal network telemetry
    snapshot = generator.collect_snapshot()

    print("NORMAL NETWORK TELEMETRY")
    print("------------------------")

    print("Device measurements:", len(snapshot["devices"]))
    print("Link measurements:", len(snapshot["links"]))

    for metric in snapshot["devices"]:
        print(
            metric.device_id,
            "CPU:", metric.cpu_percent,
            "Memory:", metric.memory_percent
        )

    for metric in snapshot["links"]:
        print(
            metric.link_id,
            "Latency:", metric.latency_ms,
            "Packet loss:", metric.packet_loss_percent,
            "Bandwidth:", metric.bandwidth_utilization_percent
        )

    assert len(snapshot["devices"]) == 5
    assert len(snapshot["links"]) == 4

    # Simulate S2 failure
    network.devices["S2"].status = DeviceStatus.DOWN

    failed_snapshot = generator.collect_snapshot()

    print("\nAFTER S2 FAILURE")
    print("----------------")

    print("Device measurements:", len(failed_snapshot["devices"]))
    print("Link measurements:", len(failed_snapshot["links"]))

    assert len(failed_snapshot["devices"]) == 4
    assert len(failed_snapshot["links"]) == 1

    print("\nAll telemetry generator checks passed!")


if __name__ == "__main__":
    main()

