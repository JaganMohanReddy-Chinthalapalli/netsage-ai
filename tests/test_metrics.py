
from simulator.devices.device import Device
from network_collector.metrics import DeviceMetrics, LinkMetrics


def main():

    # Device telemetry
    device_metrics = DeviceMetrics(
        device_id="S2",
        cpu_percent=92.5,
        memory_percent=78.0
    )

    # Link telemetry
    link_metrics = LinkMetrics(
        link_id="L2",
        latency_ms=85.0,
        packet_loss_percent=12.5,
        bandwidth_utilization_percent=90.0
    )

    print("DEVICE TELEMETRY")
    print("----------------")
    print(device_metrics)

    print("\nLINK TELEMETRY")
    print("--------------")
    print(link_metrics)

    # Validation checks
    try:
        DeviceMetrics("S3", 120.0, 50.0)
        assert False, "Invalid CPU value was accepted"
    except ValueError:
        print("\nInvalid CPU correctly rejected")

    try:
        LinkMetrics("L3", 10.0, 150.0, 50.0)
        assert False, "Invalid packet loss was accepted"
    except ValueError:
        print("Invalid packet loss correctly rejected")

    print("\nAll telemetry model checks passed!")


if __name__ == "__main__":
    main()
