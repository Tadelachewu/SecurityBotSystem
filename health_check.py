import shutil

import psutil


def check_system_health_detailed():
    alerts = []
    status = []

    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count(logical=True)
    status.append(f"🧠 CPU: {cpu_usage}% used across {cpu_count} cores")
    if cpu_usage > 85:
        alerts.append(f"⚠️ High CPU usage: {cpu_usage}%")

    # Memory
    memory = psutil.virtual_memory()
    status.append(f"💾 Memory: {memory.percent}% used\n"
                  f"Total: {memory.total // (1024 ** 3)} GB | "
                  f"Used: {memory.used // (1024 ** 3)} GB | "
                  f"Free: {memory.available // (1024 ** 3)} GB")
    if memory.percent > 85:
        alerts.append("⚠️ Memory usage too high!")

    # Disk
    disk = shutil.disk_usage("/")
    total_gb = disk.total // (1024 ** 3)
    used_gb = (disk.total - disk.free) // (1024 ** 3)
    free_gb = disk.free // (1024 ** 3)
    percent_free = (disk.free / disk.total) * 100

    status.append(f"🗂 Disk: {percent_free:.1f}% free\n"
                  f"Total: {total_gb} GB | Used: {used_gb} GB | Free: {free_gb} GB")
    if percent_free < 15:
        alerts.append("❌ Disk space critically low!")

    return status, alerts
