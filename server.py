"""
Target server with basic mitigation endpoints.
"""

from flask import Flask, request, jsonify
from target_server.logger import log

app = Flask(__name__)

blocklist = set()

@app.route("/")
def index():
    ip = request.remote_addr
    if ip in blocklist:
        return "Blocked", 403
    return "Hello from Target Server!", 200

@app.route("/_status")
def status():
    return jsonify({"status": "running", "blocked": len(blocklist)})

@app.route("/_admin/reset", methods=["POST"])
def reset():
    blocklist.clear()
    log("Blocklist reset")
    return jsonify({"ok": True})

@app.route("/_admin/blocklist")
def show_blocklist():
    return jsonify({"blocklist": list(blocklist)})

if __name__ == "__main__":
    log("Starting target server at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
