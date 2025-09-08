"""
Utility functions used by attacker modules.
"""

import logging
import socket
import urllib.parse
import ipaddress

logging.basicConfig(filename="logs/attacker.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")


def log(msg: str):
    logging.info(msg)


def parse_target(target: str):
    """
    Accepts:
      - http(s)://host:port/path
      - host:port (for UDP)
      - plain IP or hostname

    Returns dict with keys: scheme, host, port, path, raw
    """
    parsed = {"scheme": None, "host": None, "port": None, "path": None, "raw": target}
    try:
        if "://" in target:
            p = urllib.parse.urlparse(target)
            parsed["scheme"] = p.scheme
            parsed["host"] = p.hostname
            parsed["port"] = p.port
            parsed["path"] = p.path or "/"
        elif ":" in target:
            host, port = target.split(":", 1)
            parsed["host"] = host
            parsed["port"] = int(port)
        else:
            parsed["host"] = target
    except Exception:
        pass
    return parsed


def is_private_or_local(host: str) -> bool:
    """
    Safety check: only allow localhost or RFC1918 private addresses unless user overrides.
    This reduces risk of accidentally targeting public servers.
    """
    if not host:
        return False
    try:
        # resolve host to IP
        ip = socket.gethostbyname(host)
        addr = ipaddress.ip_address(ip)
        # localhost
        if addr.is_loopback:
            return True
        # private ranges
        if addr.is_private:
            return True
        # link-local or multicast -> disallow
        return False
    except Exception:
        return False
