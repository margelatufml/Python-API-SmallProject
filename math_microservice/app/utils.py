
from typing import Any, Tuple
import json
from datetime import datetime
import threading
import queue

_cache = {}

LOG_FILE = "math_microservice.log"

# Simulated messaging/streaming queue for logging
_log_queue = queue.Queue()

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
    # Put log entry in queue for streaming
    _log_queue.put(entry)

# Background thread to consume log queue and write to file
def _log_consumer():
    while True:
        entry = _log_queue.get()
        if entry is None:
            break
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        _log_queue.task_done()

_log_thread = threading.Thread(target=_log_consumer, daemon=True)
_log_thread.start()
