import json
import os
from datetime import datetime

LOG_FILE = "logs.json"

def log_request(input_text, result):
    """
    Logs the request details to logs.json.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input_text": input_text,
        "category": result["category"],
        "confidence": result["confidence"],
        "template": result["template"],
        "tokens": result["tokens"]
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
            
    logs.append(log_entry)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)
