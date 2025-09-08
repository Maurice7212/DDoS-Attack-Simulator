"""
Basic mitigation mechanisms: rate limiting and IP blocklist.
This is intentionally simple and educational.
"""

import time
from flask import request
from .logger import log
from pathlib import Path

# In-memory state
_req_times = {}  # ip -> [timestamps]
_blocklist = set()

def reset_state():
    global _req_times, _blocklist
    _req_times = {}
    _blocklist = set()

def rate_limit_check(max_per_sec: int) -> (bool, str):
    """
    Returns (allowed: bool, reason: str).
    If blocked due to rate limit, will add ip to blocklist and return False.
    """
    ip = request.remote_addr or "unknown"
    now = time.time()

    if ip in _blocklist:
        return False, "blocked"

    times = _req_times.setdefault(ip, [])
    # drop anything older than 1 second
    cutoff = now - 1.0
    while times and times[0] < cutoff:
        times.pop(0)
    times.append(now)
    if len(times) > max_per_sec:
        _blocklist.add(ip)
        log(f"Mitigation: added {ip} to blocklist (exceeded {max_per_sec}/sec)")
        return False, "rate_limit_exceeded"
    return True, "ok"

def is_blocked(ip: str) -> bool:
    return ip in _blocklist

def get_blocklist():
    return list(_blocklist)
