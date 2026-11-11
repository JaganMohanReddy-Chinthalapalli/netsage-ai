
from network_collector.metrics import DeviceMetrics, LinkMetrics
from intelligence.anomaly_detection import (
    AnomalyDetector,
    Severity
)


def main():

    detector = AnomalyDetector()

    # Simulate abnormal device measurements
    device_metrics = DeviceMetrics(
        device_id="S2",
        cpu_percent=98.0,
        memory_percent=88.0
    )

    # Simulate abnormal link measurements
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

    print("ANOMALY DETECTION RESULTS")
    print("-------------------------")

    for anomaly in anomalies:

        print(
            f"[{anomaly.severity.value.upper()}] "
            f"{anomaly.source_id} | "
            f"{anomaly.metric_name} | "
            f"Observed: {anomaly.observed_value} | "
            f"Threshold: {anomaly.threshold}"
        )

    # Verify expected anomalies
    assert len(anomalies) == 5

    critical_count = sum(
        a.severity == Severity.CRITICAL
        for a in anomalies
    )

    warning_count = sum(
        a.severity == Severity.WARNING
        for a in anomalies
    )

    assert critical_count == 3
    assert warning_count == 2

    print("\nCritical anomalies:", critical_count)
    print("Warning anomalies:", warning_count)

    # Test normal measurements
    normal_device = DeviceMetrics(
        device_id="R1",
        cpu_percent=35.0,
        memory_percent=50.0
    )

    normal_link = LinkMetrics(
        link_id="L1",
        latency_ms=10.0,
        packet_loss_percent=0.5,
        bandwidth_utilization_percent=40.0
    )

    normal_snapshot = {
        "devices": [normal_device],
        "links": [normal_link]
    }

    normal_anomalies = detector.analyze_snapshot(
        normal_snapshot
    )

    assert len(normal_anomalies) == 0

    print("\nNormal measurements produced no anomalies")

    print("\nAll anomaly detection checks passed!")


if __name__ == "__main__":
    main()
