🚀 Educational DDoS Attack Simulator

An interactive simulator to demonstrate Distributed Denial of Service (DDoS) attack concepts in a safe, controlled, and educational environment.
This project is built with Python, FastAPI, Tkinter, and Matplotlib, featuring configurable attacks, real-time charts, and server mitigation controls.

⚠️ Disclaimer: This tool is for educational purposes only. Do NOT use it against real-world servers. Test locally in a controlled lab environment.

✨ Features

🎛️ Tkinter GUI Dashboard

Configure target, attack type, RPS, duration, and nodes.

Start/stop attacks with a single click.

Toggle Auto Report Export or use Manual Export.

📊 Real-Time Charts

Live Traffic (RPS) monitoring.

System resource usage (CPU, memory).

🖥️ Target Server Controls

Reset server mitigation.

View blocklisted IPs.

📑 Reporting

Export results as a PDF report with charts and metadata.

📸 Screenshots
Dashboard	Report Export

	
## Screenshots

### Dashboard
![Dashboard](screenshots/1.png)

### Attack Running
![Attack Running](screenshots/ONE.png)

### Report Export
![Report Export](screenshots/TWO.png)


📂 Project Structure
DDoS-Attack-Simulator/
│── run.py                 # Entry point
│── attacker/              # Attack simulation logic
│── target_server/         # Target server + mitigation endpoints
│── gui/                   # Tkinter dashboard + charts + report export
│── reports/               # Generated PDF reports
│── screenshots/           # Project screenshots
└── requirements.txt       # Dependencies

🚀 Getting Started
1. Clone the Repository
git clone https://github.com/yourusername/ddos-attack-simulator.git
cd ddos-attack-simulator

2. Create Virtual Environment & Install Dependencies
python -m venv .venv
source .venv/bin/activate  # (Linux/Mac)
.venv\Scripts\activate     # (Windows)

pip install -r requirements.txt

3. Run the Simulator
python run.py


Choose one of: server / attacker / gui / all

🛠️ Dependencies

Python 3.9+

Tkinter

FastAPI

Matplotlib

Requests

PyYAML

ReportLab

Install via:

pip install -r requirements.txt

📖 Usage

Start the server (python run.py server)

Launch the GUI (python run.py gui)

Configure attack parameters

Start/Stop attacks and monitor live charts

Export results as PDF reports

⚠️ Disclaimer

This project is strictly for learning, research, and demonstration.
Do NOT deploy or use it against production systems or third-party servers.

📜 License

MIT License © 2025
