from simulator.devices.device import Device, DeviceType, DeviceStatus
from topology.link import NetworkLink
from topology.network_topology import NetworkTopology
from simulator.scenarios.scenario_engine import ScenarioEngine
from simulator.scenarios.events import EventType


def main():

    # 1. Build network

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

    # 2. Initialize scenario engine

    engine = ScenarioEngine(network)

    print("NORMAL NETWORK")
    print("--------------")

    print("Reachable devices:", sorted(
        network.get_reachable_devices("R1")
    ))

    # 3. Inject S2 failure

    print("\nINJECTING FAILURE")
    print("-----------------")

    failure_event = engine.fail_device("S2")

    print(failure_event.description)

    print("Event type:", failure_event.event_type.value)
    print("Timestamp:", failure_event.timestamp.isoformat())

    # 4. Analyze network impact

    unreachable = network.find_unreachable_devices("R1")

    print("\nIMPACT ANALYSIS")
    print("---------------")

    for device in unreachable:
        print(device.hostname, "is unreachable from R1")

    # 5. Recover S2

    print("\nRECOVERING DEVICE")
    print("-----------------")

    recovery_event = engine.recover_device("S2")

    print(recovery_event.description)

    # 6. Verify recovery

    reachable = network.get_reachable_devices("R1")

    print("\nRECOVERED NETWORK")
    print("-----------------")

    print("Reachable devices:", sorted(reachable))

    # 7. Verify events

    print("\nEVENT HISTORY")
    print("-------------")

    for event in engine.get_events():
        print(
            event.timestamp.isoformat(),
            event.event_type.value,
            event.device_id
        )

    assert failure_event.event_type == EventType.DEVICE_DOWN

    assert recovery_event.event_type == EventType.DEVICE_UP

    assert {
        device.device_id for device in unreachable
    } == {"SRV1", "SRV2"}

    assert reachable == {"R1", "S1", "S2", "SRV1", "SRV2"}

    assert len(engine.get_events()) == 2

    assert network.devices["S2"].status == DeviceStatus.UP

    print("\nAll scenario engine checks passed!")


if __name__ == "__main__":
    main()
