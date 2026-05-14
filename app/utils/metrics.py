import json
import os
from datetime import datetime

LOG_FILE = "data/query_logs.json"


def log_query_metrics(query, query_type, model_used, response_time):
    os.makedirs("data", exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "query_type": query_type,
        "model_used": model_used,
        "response_time_seconds": round(response_time, 2)
    }

    logs = []

    # Load existing logs
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            try:
                logs = json.load(file)
            except:
                logs = []

    logs.append(log_entry)

    # Save updated logs
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)