from simulator.devices.device import (
    Device,
    DeviceType,
    DeviceStatus
)

from topology.link import NetworkLink

from topology.network_topology import NetworkTopology


def main():

    network = NetworkTopology()

    # Create devices

    devices = [
        Device("R1", "R1", DeviceType.ROUTER, "192.168.1.1"),
        Device("S1", "S1", DeviceType.SWITCH, "192.168.1.2"),
        Device("S2", "S2", DeviceType.SWITCH, "192.168.1.3"),
        Device("SRV1", "SRV1", DeviceType.SERVER, "192.168.1.10"),
        Device("SRV2", "SRV2", DeviceType.SERVER, "192.168.1.11"),
    ]

    for device in devices:
        network.add_device(device)

    # Create network links

    links = [
        NetworkLink("L1", "R1", "S1", 1000),
        NetworkLink("L2", "S1", "S2", 1000),
        NetworkLink("L3", "S2", "SRV1", 1000),
        NetworkLink("L4", "S2", "SRV2", 1000),
    ]

    for link in links:
        network.add_link(link)

    # Simulate S2 failure

    network.devices["S2"].status = DeviceStatus.DOWN

    print("NETWORK FAILURE SIMULATION")
    print("--------------------------")

    print("Failed device: S2")

    reachable = network.get_reachable_devices("R1")

    print("\nReachable devices from R1:")

    for device_id in sorted(reachable):
        print("-", device_id)

    unreachable = network.find_unreachable_devices("R1")

    print("\nUnreachable operational devices:")

    for device in unreachable:
        print("-", device.hostname)

    assert reachable == {"R1", "S1"}

    assert {
        device.device_id for device in unreachable
    } == {"SRV1", "SRV2"}

    print("\nAll impact analysis checks passed!")


if __name__ == "__main__":
    main()
