from simulator.devices.device import Device, DeviceType
from topology.link import NetworkLink
from topology.network_topology import NetworkTopology


def main():

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

    print("Network topology created successfully!")

    print("\nDevices:", len(network.devices))
    print("Links:", len(network.links))

    print("\nDevices connected to S2:")

    for device in network.get_neighbors("S2"):
        print(f"- {device.hostname} ({device.device_type.value})")


if __name__ == "__main__":
    main()
