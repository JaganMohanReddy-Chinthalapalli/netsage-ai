
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from network_collector.metrics import DeviceMetrics, LinkMetrics


class Severity(Enum):
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True)
class Anomaly:
    source_type: str
    source_id: str
    metric_name: str
    observed_value: float
    threshold: float
    severity: Severity
    timestamp: datetime
    description: str


class AnomalyDetector:

    def __init__(self):

        self.thresholds = {
            "cpu_percent": (85, 95),
            "memory_percent": (85, 95),
            "latency_ms": (100, 250),
            "packet_loss_percent": (2, 10),
            "bandwidth_utilization_percent": (85, 95)
        }

    def _check_metric(
        self,
        source_type,
        source_id,
        metric_name,
        value,
        timestamp
    ):

        warning_threshold, critical_threshold = (
            self.thresholds[metric_name]
        )

        if value >= critical_threshold:
            severity = Severity.CRITICAL
            threshold = critical_threshold

        elif value >= warning_threshold:
            severity = Severity.WARNING
            threshold = warning_threshold

        else:
            return None

        return Anomaly(
            source_type=source_type,
            source_id=source_id,
            metric_name=metric_name,
            observed_value=value,
            threshold=threshold,
            severity=severity,
            timestamp=timestamp,
            description=(
                f"{metric_name} on {source_id} is "
                f"{value}, exceeding the {severity.value} "
                f"threshold of {threshold}"
            )
        )

    def detect_device_anomalies(self, metrics: DeviceMetrics):

        anomalies = []

        for metric_name in (
            "cpu_percent",
            "memory_percent"
        ):

            value = getattr(metrics, metric_name)

            anomaly = self._check_metric(
                "device",
                metrics.device_id,
                metric_name,
                value,
                metrics.timestamp
            )

            if anomaly:
                anomalies.append(anomaly)

        return anomalies

    def detect_link_anomalies(self, metrics: LinkMetrics):

        anomalies = []

        for metric_name in (
            "latency_ms",
            "packet_loss_percent",
            "bandwidth_utilization_percent"
        ):

            value = getattr(metrics, metric_name)

            anomaly = self._check_metric(
                "link",
                metrics.link_id,
                metric_name,
                value,
                metrics.timestamp
            )

            if anomaly:
                anomalies.append(anomaly)

        return anomalies

    def analyze_snapshot(self, snapshot):

        anomalies = []

        for metrics in snapshot["devices"]:
            anomalies.extend(
                self.detect_device_anomalies(metrics)
            )

        for metrics in snapshot["links"]:
            anomalies.extend(
                self.detect_link_anomalies(metrics)
            )

        return anomalies
