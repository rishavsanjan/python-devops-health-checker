from datetime import datetime, timezone

def create_result(name, status, message, value=None):
    return {
        "name": name,
        "status": status,
        "message": message,
        "value": value,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }