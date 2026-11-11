
from simulator.devices.device import Device, DeviceType
from topology.link import NetworkLink
from topology.network_topology import NetworkTopology

from simulator.scenarios.scenario_engine import ScenarioEngine
from simulator.telemetry_generator import TelemetryGenerator

from network_collector.metrics import DeviceMetrics, LinkMetrics

from intelligence.anomaly_detection import AnomalyDetector
from intelligence.incidents import IncidentManager


def main():

    # 1. Build network topology

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

    # 2. Initialize components

    scenario_engine = ScenarioEngine(network)
    telemetry_generator = TelemetryGenerator(network, seed=42)
    anomaly_detector = AnomalyDetector()
    incident_manager = IncidentManager()

    # 3. Collect normal telemetry

    print("NORMAL NETWORK")
    print("--------------")

    normal_snapshot = telemetry_generator.collect_snapshot()

    print("Device measurements:", len(normal_snapshot["devices"]))
    print("Link measurements:", len(normal_snapshot["links"]))

    normal_anomalies = anomaly_detector.analyze_snapshot(
        normal_snapshot
    )

    assert len(normal_anomalies) == 0

    normal_incidents = incident_manager.process_anomalies(
        normal_anomalies
    )

    assert len(normal_incidents) == 0

    print("No anomalies or incidents detected")

    # 4. Inject S2 failure

    print("\nSIMULATING NETWORK FAILURE")
    print("--------------------------")

    event = scenario_engine.fail_device("S2")

    print(event.description)

    # 5. Collect telemetry after failure

    failed_snapshot = telemetry_generator.collect_snapshot()

    print("\nPOST-FAILURE TELEMETRY")
    print("----------------------")

    print("Device measurements:", len(failed_snapshot["devices"]))
    print("Link measurements:", len(failed_snapshot["links"]))

    assert len(failed_snapshot["devices"]) == 4
    assert len(failed_snapshot["links"]) == 1

    # 6. Inject abnormal telemetry for demonstration

    failed_snapshot["devices"].append(
        DeviceMetrics(
            device_id="R1",
            cpu_percent=98.0,
            memory_percent=88.0
        )
    )

    failed_snapshot["links"].append(
        LinkMetrics(
            link_id="L1",
            latency_ms=280.0,
            packet_loss_percent=5.0,
            bandwidth_utilization_percent=97.0
        )
    )

    # 7. Detect anomalies

    anomalies = anomaly_detector.analyze_snapshot(
        failed_snapshot
    )

    print("\nDETECTED ANOMALIES")
    print("------------------")

    for anomaly in anomalies:
        print(
            anomaly.source_id,
            anomaly.metric_name,
            anomaly.severity.value
        )

    # 8. Generate incidents

    incidents = incident_manager.process_anomalies(anomalies)

    print("\nGENERATED INCIDENTS")
    print("-------------------")

    for incident in incidents:
        print(
            incident.incident_id,
            incident.source_type,
            incident.source_id,
            incident.severity.value
        )

    # 9. Verify impact analysis

    unreachable = network.find_unreachable_devices("R1")

    print("\nNETWORK IMPACT")
    print("--------------")

    for device in unreachable:
        print(device.hostname, "is unreachable from R1")

    assert {
        device.device_id for device in unreachable
    } == {"SRV1", "SRV2"}

    # 10. Verify integration

    assert len(anomalies) == 5
    assert len(incidents) == 2
    assert len(incident_manager.get_all_incidents()) == 2

    print("\nALL END-TO-END CHECKS PASSED!")


if __name__ == "__main__":
    main()
