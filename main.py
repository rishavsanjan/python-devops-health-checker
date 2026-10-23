import shutil
import subprocess
from system_checks import (
    check_cpu,
    check_memory,
    check_disk,
    get_status,
    check_platform
)


def check_command(command):
    return shutil.which(command)


def check_tool_version(command):
    try:
        result = subprocess.run(
            [command, "--version"],
                capture_output=True, 
                text=True,
                timeout=10
        )

        if result.returncode == 0:
            return result.stdout.strip()

        return "Command failed"
       
    except subprocess.TimeoutExpired:
        return "Connection timed out"
    except OSError:
        return "Unable to execute command"


def check_docker():
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, 
            text=True,
            timeout=10
        )

        if result.returncode == 0:
             return True, "Docker daemon is running!"

        error = result.stderr.strip()

        return False, error or "Docker daemon is not running!"

    except subprocess.TimeoutExpired:
            return False, "Connection timed out"
    except OSError:
            return False, "Unable to execute command"


def print_resource_check(name, usage):
    status = get_status(usage)
    print(f"[{status}] {name}: {usage:.1f}% used")


def main():
    commands = ["python", "docker", "kubectl", "aws"]

    for command in commands:
        if check_command(command):
            version = check_tool_version(command)
            print(f"[OK] {command}: {version}")
        else:
            print(f"[MISSING] {command}")

main()

print("\n--- Docker Health Check ---")
healthy, message = check_docker()
if healthy:
    print(f"[OK] {message}")
else:
    print(f"[FAIL] {message}")


current_platform = check_platform()
cpu_usage = check_cpu()
memory_usage = check_memory()
disk_usage = check_disk()

print("Current platform : ", current_platform)
print("CPU Usage:", cpu_usage, "%", get_status(cpu_usage))
print("Memory Usage:", memory_usage, "%", get_status(memory_usage))
print("Disk Usage:", disk_usage, "%", get_status(disk_usage))