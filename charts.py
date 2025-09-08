import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import threading
import time
from tkinter import ttk

class TrafficChart:
    def __init__(self, parent):
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Traffic (requests/sec)")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("RPS")
        self.xdata, self.ydata = [], []

        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_chart(self, value):
        self.xdata.append(len(self.xdata))
        self.ydata.append(value)
        self.ax.clear()
        self.ax.set_title("Traffic (requests/sec)")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("RPS")
        self.ax.plot(self.xdata, self.ydata, color="blue")
        self.canvas.draw()


class ResourceTabs:
    def __init__(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.cpu_mem_tab = ttk.Frame(self.notebook)
        self.disk_tab = ttk.Frame(self.notebook)
        self.net_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.cpu_mem_tab, text="CPU & Memory")
        self.notebook.add(self.disk_tab, text="Disk I/O")
        self.notebook.add(self.net_tab, text="Network I/O")

        # Figures for each tab
        self.cpu_mem_fig = Figure(figsize=(5, 3), dpi=100)
        self.disk_fig = Figure(figsize=(5, 3), dpi=100)
        self.net_fig = Figure(figsize=(5, 3), dpi=100)

        self.cpu_mem_ax = self.cpu_mem_fig.add_subplot(111)
        self.disk_ax = self.disk_fig.add_subplot(111)
        self.net_ax = self.net_fig.add_subplot(111)

        # Canvas
        self.cpu_mem_canvas = FigureCanvasTkAgg(self.cpu_mem_fig, master=self.cpu_mem_tab)
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, master=self.disk_tab)
        self.net_canvas = FigureCanvasTkAgg(self.net_fig, master=self.net_tab)

        self.cpu_mem_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.disk_canvas.get_tk_widget().pack(fill="both", expand=True)
        self.net_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Data storage
        self.xdata = []
        self.cpu_data, self.mem_data = [], []
        self.disk_read, self.disk_write = [], []
        self.net_sent, self.net_recv = [], []

        # Counters for deltas
        self.last_disk = psutil.disk_io_counters()
        self.last_net = psutil.net_io_counters()

        # Start background polling
        self._running = True
        threading.Thread(target=self._poll_system_usage, daemon=True).start()

    def _poll_system_usage(self):
        while self._running:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent

            # Disk I/O (MB/s)
            new_disk = psutil.disk_io_counters()
            read_mb = (new_disk.read_bytes - self.last_disk.read_bytes) / (1024 * 1024)
            write_mb = (new_disk.write_bytes - self.last_disk.write_bytes) / (1024 * 1024)
            self.last_disk = new_disk

            # Network I/O (KB/s)
            new_net = psutil.net_io_counters()
            sent_kb = (new_net.bytes_sent - self.last_net.bytes_sent) / 1024
            recv_kb = (new_net.bytes_recv - self.last_net.bytes_recv) / 1024
            self.last_net = new_net

            self.update_charts(cpu, mem, read_mb, write_mb, sent_kb, recv_kb)

    def update_charts(self, cpu, mem, read_mb, write_mb, sent_kb, recv_kb):
        self.xdata.append(len(self.xdata))
        self.cpu_data.append(cpu)
        self.mem_data.append(mem)
        self.disk_read.append(read_mb)
        self.disk_write.append(write_mb)
        self.net_sent.append(sent_kb)
        self.net_recv.append(recv_kb)

        # CPU & Memory
        self.cpu_mem_ax.clear()
        self.cpu_mem_ax.set_title("CPU & Memory Usage")
        self.cpu_mem_ax.plot(self.xdata, self.cpu_data, label="CPU %", color="red")
        self.cpu_mem_ax.plot(self.xdata, self.mem_data, label="Memory %", color="green")
        self.cpu_mem_ax.legend(loc="upper right", fontsize=8)
        self.cpu_mem_canvas.draw()

        # Disk I/O
        self.disk_ax.clear()
        self.disk_ax.set_title("Disk I/O (MB/s)")
        self.disk_ax.plot(self.xdata, self.disk_read, label="Read MB/s", color="blue")
        self.disk_ax.plot(self.xdata, self.disk_write, label="Write MB/s", color="orange")
        self.disk_ax.legend(loc="upper right", fontsize=8)
        self.disk_canvas.draw()

        # Network I/O
        self.net_ax.clear()
        self.net_ax.set_title("Network I/O (KB/s)")
        self.net_ax.plot(self.xdata, self.net_sent, label="Upload KB/s", color="purple")
        self.net_ax.plot(self.xdata, self.net_recv, label="Download KB/s", color="brown")
        self.net_ax.legend(loc="upper right", fontsize=8)
        self.net_canvas.draw()

    def stop(self):
        self._running = False
