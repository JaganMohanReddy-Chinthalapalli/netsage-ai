
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from intelligence.anomaly_detection import Anomaly, Severity


class IncidentStatus(Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


@dataclass
class Incident:

    incident_id: str
    source_type: str
    source_id: str
    severity: Severity
    anomalies: list[Anomaly] = field(default_factory=list)

    status: IncidentStatus = IncidentStatus.OPEN

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_anomaly(self, anomaly: Anomaly):

        self.anomalies.append(anomaly)

        if anomaly.severity == Severity.CRITICAL:
            self.severity = Severity.CRITICAL

        self.updated_at = datetime.now(timezone.utc)


class IncidentManager:

    def __init__(self):
        self.incidents = {}

    def process_anomalies(self, anomalies):

        grouped = {}

        for anomaly in anomalies:

            key = (anomaly.source_type, anomaly.source_id)

            grouped.setdefault(key, []).append(anomaly)

        affected_incidents = []

        for (source_type, source_id), source_anomalies in grouped.items():

            # Find an existing active incident for this resource
            incident = next(
                (
                    item for item in self.incidents.values()
                    if item.source_type == source_type
                    and item.source_id == source_id
                    and item.status != IncidentStatus.RESOLVED
                ),
                None
            )

            # Create a new incident if none exists
            if incident is None:

                incident = Incident(
                    incident_id=f"INC-{uuid4().hex[:8].upper()}",
                    source_type=source_type,
                    source_id=source_id,
                    severity=Severity.WARNING
                )

                self.incidents[incident.incident_id] = incident

            # Add the detected anomalies
            for anomaly in source_anomalies:
                incident.add_anomaly(anomaly)

            affected_incidents.append(incident)

        return affected_incidents

    def acknowledge_incident(self, incident_id):

        incident = self._get_incident(incident_id)

        if incident.status == IncidentStatus.RESOLVED:
            raise ValueError("Cannot acknowledge a resolved incident")

        incident.status = IncidentStatus.ACKNOWLEDGED

    def resolve_incident(self, incident_id):

        incident = self._get_incident(incident_id)

        incident.status = IncidentStatus.RESOLVED

    def _get_incident(self, incident_id):

        if incident_id not in self.incidents:
            raise ValueError(f"Unknown incident: {incident_id}")

        return self.incidents[incident_id]

    def get_all_incidents(self):

        return list(self.incidents.values())
