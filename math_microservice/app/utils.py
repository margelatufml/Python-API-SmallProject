from typing import Any, Tuple
import json
from datetime import datetime

_cache = {}

LOG_FILE = "math_microservice.log"

def cache_get(key: Tuple) -> Any:
    return _cache.get(key)

def cache_set(key: Tuple, value: Any):
    _cache[key] = value

def log_operation(operation: str, input_data: dict, result: dict):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "input": input_data,
        "result": result
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
