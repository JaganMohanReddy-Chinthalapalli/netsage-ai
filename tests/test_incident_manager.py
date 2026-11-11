
from network_collector.metrics import DeviceMetrics, LinkMetrics

from intelligence.anomaly_detection import (
    AnomalyDetector,
    Severity
)

from intelligence.incidents import (
    IncidentManager,
    IncidentStatus
)


def main():

    detector = AnomalyDetector()
    manager = IncidentManager()

    # Generate abnormal telemetry
    device_metrics = DeviceMetrics(
        device_id="S2",
        cpu_percent=98.0,
        memory_percent=88.0
    )

    link_metrics = LinkMetrics(
        link_id="L2",
        latency_ms=280.0,
        packet_loss_percent=5.0,
        bandwidth_utilization_percent=97.0
    )

    snapshot = {
        "devices": [device_metrics],
        "links": [link_metrics]
    }

    anomalies = detector.analyze_snapshot(snapshot)

    # Convert anomalies into incidents
    incidents = manager.process_anomalies(anomalies)

    print("GENERATED INCIDENTS")
    print("-------------------")

    for incident in incidents:

        print(
            incident.incident_id,
            incident.source_type,
            incident.source_id,
            incident.severity.value
        )

        for anomaly in incident.anomalies:
            print(
                "  -",
                anomaly.metric_name,
                anomaly.observed_value,
                anomaly.severity.value
            )

    # Verify grouping
    assert len(incidents) == 2

    s2_incident = next(
        item for item in incidents
        if item.source_id == "S2"
    )

    l2_incident = next(
        item for item in incidents
        if item.source_id == "L2"
    )

    assert len(s2_incident.anomalies) == 2
    assert len(l2_incident.anomalies) == 3

    assert s2_incident.severity == Severity.CRITICAL
    assert l2_incident.severity == Severity.CRITICAL

    # Verify repeated alerts update an existing incident
    manager.process_anomalies(anomalies)

    assert len(manager.get_all_incidents()) == 2
    assert len(s2_incident.anomalies) == 4

    # Acknowledge an incident
    manager.acknowledge_incident(s2_incident.incident_id)

    assert s2_incident.status == IncidentStatus.ACKNOWLEDGED

    # Resolve an incident
    manager.resolve_incident(s2_incident.incident_id)

    assert s2_incident.status == IncidentStatus.RESOLVED

    print("\nS2 incident acknowledged and resolved successfully")
    print("Repeated alerts correctly updated existing incidents")
    print("\nAll incident management checks passed!")


if __name__ == "__main__":
    main()
