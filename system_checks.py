import psutil
import platform

def get_status(usage):
    if usage >= 80 and usage < 90:
        return "WARNING"
    elif usage >= 90:
        return "CRITICAL"
    else:
        return "OK"

def check_platform():
    return platform.system()

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    return usage


def check_memory():
    memory = psutil.virtual_memory()
    return memory.percent


def check_disk():
    disk = psutil.disk_usage("/")
    return disk.percent

# current_platform = check_platform()
# cpu_usage = check_cpu()
# memory_usage = check_memory()
# disk_usage = check_disk()

# print("Current platform : ", current_platform)
# print("CPU Usage:", cpu_usage, "%", get_status(cpu_usage))
# print("Memory Usage:", memory_usage, "%", get_status(memory_usage))
# print("Disk Usage:", disk_usage, "%", get_status(disk_usage))