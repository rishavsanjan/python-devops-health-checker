import subprocess
import json

def check_containers():
    try:
        result = subprocess.run(
            [
                "docker", "ps", "-a",
                "--format", "{{json .}}"
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=False
        )

        if result.returncode != 0:
            return False, [], result.stderr.strip()

        containers = []

        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            container = json.loads(line)

            state = container.get("State", "").lower()

            if state == "running":
                status = "OK"
            elif state in ("created", "restarting"):
                status = "WARNING"
            else:
                status = "CRITICAL"

            containers.append({
                "name": container.get("Names", "unknown"),
                "state": state,
                "status": status
            })

        return True, containers, ""

    except subprocess.TimeoutExpired:
        return False, [], "Docker command timed out"

    except OSError as error:
        return False, [], str(error)

    except json.JSONDecodeError:
        return False, [], "Could not parse Docker output"