import psutil
import platform


def get_cpu_usage():
    cpu = psutil.cpu_percent(interval=1)

    return {
        "success": True,
        "cpu_usage": cpu,
        "message": f"CPU usage is currently {cpu}%."
    }


def get_ram_usage():
    memory = psutil.virtual_memory()

    used_percent = memory.percent

    return {
        "success": True,
        "ram_usage": used_percent,
        "message": f"RAM usage is currently {used_percent}%."
    }


def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "success": False,
            "message": "Battery information is not available."
        }

    plugged_in = battery.power_plugged
    percent = battery.percent

    charging_status = (
        "plugged in"
        if plugged_in
        else "running on battery"
    )

    return {
        "success": True,
        "battery": percent,
        "plugged_in": plugged_in,
        "message": (
            f"Battery is at {percent}% and the computer "
            f"is {charging_status}."
        )
    }


def get_system_status():

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()

    battery = psutil.sensors_battery()

    system_info = {
        "success": True,
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "cpu_usage": cpu,
        "ram_usage": memory.percent
    }

    if battery:
        system_info["battery"] = battery.percent
        system_info["plugged_in"] = battery.power_plugged

    return system_info