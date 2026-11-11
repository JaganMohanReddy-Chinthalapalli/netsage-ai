from simulator.devices.device import (
    Device,
    DeviceType,
    DeviceStatus
)


def main():
    router = Device(
        device_id="DEV-001",
        hostname="R1",
        device_type=DeviceType.ROUTER,
        management_ip="192.168.1.1",
        cpu_percent=35.0,
        memory_percent=60.0
    )

    print("Device created successfully!")
    print(router)

    assert router.hostname == "R1"
    assert router.status == DeviceStatus.UP
    assert router.cpu_percent == 35.0

    print("\nAll basic checks passed!")


if __name__ == "__main__":
    main()
