from datetime import datetime, timezone
import json
from pathlib import Path

def create_result(name, status, message, value=None):
    return {
        "name": name,
        "status": status,
        "message": message,
        "value": value,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def save_report(results):
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "health_report.json"

    with report_file.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    return report_file