"""
Tkinter GUI to control the attacker and view live charts.
This integrates with attacker.attacks.run_attack and target_server admin endpoints.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import yaml
import matplotlib.pyplot as plt
from attacker.attacks import run_attack, stop_attacks
from gui.charts import TrafficChart, ResourceTabs

# Default config path
ATTACKER_CONFIG = "attacker/config.yaml"
SERVER_STATUS_PATH = "/_status"
ADMIN_RESET_PATH = "/_admin/reset"
ADMIN_BLOCKLIST_PATH = "/_admin/blocklist"


class DDosSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational DDoS Simulator - GUI")
        self.root.geometry("1100x750")
        self._attack_thread = None
        self._running = False

        # read default config
        try:
            with open(ATTACKER_CONFIG) as f:
                self.default_cfg = yaml.safe_load(f)
        except Exception:
            self.default_cfg = {}

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=8, pady=6)

        ttk.Label(top, text="Target (URL or host:port):").grid(row=0, column=0, sticky="w")
        self.target_var = tk.StringVar(
            value=self.default_cfg.get("target", "http://127.0.0.1:5000")
        )
        ttk.Entry(top, textvariable=self.target_var, width=40).grid(
            row=0, column=1, padx=6
        )

        ttk.Label(top, text="Attack Type:").grid(row=1, column=0, sticky="w")
        self.attack_type = tk.StringVar(
            value=self.default_cfg.get("attack_type", "http")
        )
        ttk.Combobox(
            top,
            textvariable=self.attack_type,
            values=["http", "udp", "syn", "mixed"],
            width=12,
        ).grid(row=1, column=1, sticky="w", padx=6)

        ttk.Label(top, text="Requests/sec:").grid(row=2, column=0, sticky="w")
        self.rps_var = tk.IntVar(
            value=int(self.default_cfg.get("requests_per_second", 10))
        )
        ttk.Entry(top, textvariable=self.rps_var, width=10).grid(
            row=2, column=1, sticky="w", padx=6
        )

        ttk.Label(top, text="Duration (s):").grid(row=3, column=0, sticky="w")
        self.duration_var = tk.IntVar(
            value=int(self.default_cfg.get("duration_seconds", 30))
        )
        ttk.Entry(top, textvariable=self.duration_var, width=10).grid(
            row=3, column=1, sticky="w", padx=6
        )

        ttk.Label(top, text="Nodes (simulated):").grid(row=4, column=0, sticky="w")
        self.nodes_var = tk.IntVar(value=int(self.default_cfg.get("num_nodes", 1)))
        ttk.Entry(top, textvariable=self.nodes_var, width=10).grid(
            row=4, column=1, sticky="w", padx=6
        )

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=0, column=2, rowspan=6, padx=12)

        self.start_btn = ttk.Button(
            btn_frame, text="Start Attack", command=self.start_attack
        )
        self.start_btn.pack(fill="x", pady=4)
        self.stop_btn = ttk.Button(
            btn_frame, text="Stop Attack", command=self.stop_attack, state="disabled"
        )
        self.stop_btn.pack(fill="x", pady=4)

        self.reset_server_btn = ttk.Button(
            btn_frame, text="Reset Server Mitigation", command=self.reset_server
        )
        self.reset_server_btn.pack(fill="x", pady=4)
        self.show_blocklist_btn = ttk.Button(
            btn_frame, text="Show Server Blocklist", command=self.show_blocklist
        )
        self.show_blocklist_btn.pack(fill="x", pady=4)

        # Export options
        self.auto_export = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            btn_frame,
            text="Auto Export Report",
            variable=self.auto_export,
        ).pack(fill="x", pady=4)

        self.export_btn = ttk.Button(
            btn_frame, text="Export Report Now", command=self.export_report
        )
        self.export_btn.pack(fill="x", pady=4)

        # Charts area
        charts_frame = ttk.Frame(self.root)
        charts_frame.pack(fill="both", expand=True, padx=8, pady=6)

        left = ttk.LabelFrame(charts_frame, text="Traffic (RPS)")
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        right = ttk.LabelFrame(charts_frame, text="System Resources")
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        self.traffic_chart = TrafficChart(left)
        self.resource_tabs = ResourceTabs(right)

    def start_attack(self):
        if self._running:
            messagebox.showinfo("Running", "Attack already running.")
            return
        target = self.target_var.get().strip()
        attack_type = self.attack_type.get()
        rps = int(self.rps_var.get())
        duration = int(self.duration_var.get())
        nodes = int(self.nodes_var.get())

        try:
            status_url = self._admin_url(target, SERVER_STATUS_PATH)
            requests.get(status_url, timeout=1.0)
        except Exception:
            if not messagebox.askyesno(
                "Warning", "Target server status endpoint not reachable. Continue?"
            ):
                return

        self._running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        self.traffic_chart.xdata = []
        self.traffic_chart.ydata = []

        def chart_cb(rps_sample):
            try:
                self.traffic_chart.update_chart(rps_sample)
            except Exception:
                pass

        def attack_runner():
            try:
                run_attack(
                    target,
                    attack_type,
                    rps,
                    duration,
                    num_nodes=nodes,
                    chart_callback=chart_cb,
                )
            except Exception as e:
                messagebox.showerror("Error", f"Attack runner error: {e}")
            finally:
                self._running = False
                self.start_btn.config(state="normal")
                self.stop_btn.config(state="disabled")
                if self.auto_export.get():
                    self.export_report()

        self._attack_thread = threading.Thread(target=attack_runner, daemon=True)
        self._attack_thread.start()

    def stop_attack(self):
        if not self._running:
            return
        stop_attacks()
        self._running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        messagebox.showinfo("Stopped", "Stop signal sent to attack threads.")

    def _admin_url(self, target, path):
        if target.startswith("http://") or target.startswith("https://"):
            return target.rstrip("/") + path
        if ":" in target:
            return "http://" + target.rstrip("/") + path
        return "http://" + target + ":80" + path

    def reset_server(self):
        target = self.target_var.get().strip()
        url = self._admin_url(target, ADMIN_RESET_PATH)
        try:
            r = requests.post(url, timeout=1.0)
            messagebox.showinfo("Reset", f"Server reset: {r.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Reset failed: {e}")

    def show_blocklist(self):
        target = self.target_var.get().strip()
        url = self._admin_url(target, ADMIN_BLOCKLIST_PATH)
        try:
            r = requests.get(url, timeout=1.0)
            data = r.json()
            bl = data.get("blocklist", [])
            messagebox.showinfo("Blocklist", "\n".join(bl) if bl else "No blocked IPs")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch blocklist: {e}")

    def export_report(self):
        try:
            # Save traffic chart
            self.traffic_chart.figure.savefig("traffic_chart.png")

            # Save each system chart
            self.resource_tabs.cpu_mem_fig.savefig("cpu_mem_chart.png")
            self.resource_tabs.disk_fig.savefig("disk_chart.png")
            self.resource_tabs.net_fig.savefig("network_chart.png")

            messagebox.showinfo(
                "Exported", "Report charts saved as PNGs in the current directory."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DDosSimulatorGUI(root)
    root.mainloop()
