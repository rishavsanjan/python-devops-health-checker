import shutil
import subprocess
import argparse
import sys
import json
from system_checks import (
    check_cpu,
    check_memory,
    check_disk,
    get_status,
    check_platform
)
from report import (create_result, save_report)
from docker_checks import check_containers


results = []
def check_command(command):
    return shutil.which(command)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Python DevOps Health Checker"
    )

    parser.add_argument(
        "--check",
        choices=["all", "docker", "system"],
        default="all",
        help="Choose which health checks to execute"
    )

    parser.add_argument(
        "--output",
        default="reports/health_report.json",
        help="Path where the JSON report will be saved"
    )

    return parser.parse_args()

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


def run_container_checks(results):
    success, containers, error = check_containers()

    if not success:
        results.append(
            create_result(
                "Docker Containers",
                "CRITICAL",
                error
            )
        )
        print(f"[CRITICAL] Docker Containers: {error}")
        return

    if not containers:
        results.append(
            create_result(
                "Docker Containers",
                "OK",
                "No containers found",
                0
            )
        )
        print("[OK] No containers found")
        return

    for container in containers:
        name = container["name"]
        state = container["state"]
        status = container["status"]

        results.append(
            create_result(
                f"Container: {name}",
                status,
                f"Container state: {state}"
            )
        )

        print(f"[{status}] {name}: {state}")


def print_resource_check(name, usage):
    status = get_status(usage)
    print(f"[{status}] {name}: {usage:.1f}% used")


def main():
    commands = ["python", "docker", "kubectl", "aws"]

    args = parse_args()

    if args.check == "docker":
        print("\n--- Docker Health Check ---")
        healthy, message = check_docker()
        if healthy:
            print(f"[OK] {message}")
            success, containers, error = check_containers()

            if not success:
                print("Docker check failed:", error)
                sys.exit(1)
            else:
                for container in containers:
                    print(
                        f"[{container['status']}] "
                        f"{container['name']}: {container['state']}"
                    )
            run_container_checks(results)
            sys.exit(0)
        else:
            print(f"[FAIL] {message}")
            sys.exit(1)
    elif args.check == "system":
        current_platform = check_platform()
        cpu_usage = check_cpu()
        memory_usage = check_memory()
        disk_usage = check_disk()

        print("Current platform : ", current_platform)
        print("CPU Usage:", cpu_usage, "%", get_status(cpu_usage))
        print("Memory Usage:", memory_usage, "%", get_status(memory_usage))
        print("Disk Usage:", disk_usage, "%", get_status(disk_usage))
        cpu_result = create_result(
        "CPU",
        get_status(cpu_usage),
        f"CPU usage is {cpu_usage:.1f}%",
        cpu_usage
        )

        results.append(cpu_result)

        memory_result = create_result(
             "Memory",
             get_status(memory_usage),
             f"Memory usage is {memory_usage:.1f}%",
             memory_usage
        )

        results.append(memory_result)

        disk_result = create_result(
             "Disk",
             get_status(disk_usage),
             f"Disk usage is {disk_usage:.1f}%",
             disk_usage
        )

        results.append(disk_result)

        report_file = save_report(results)
        print(f"\nReport saved to: {report_file}")

        failed_checks = [
             result for result in results
             if result["status"] != "OK"
        ]

        if failed_checks:
            print(f"\nHealth check failed: {len(failed_checks)} issue(s)")
            sys.exit(1)

        print("\nAll health checks passed.")
        sys.exit(0)
        
    # for command in commands:
    #     if check_command(command):
    #         version = check_tool_version(command)
    #         print(f"[OK] {command}: {version}")
    #     else:
    #         print(f"[MISSING] {command}")
    

main()










