import sys
import os
import subprocess

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run():
    print("""
    🚀 Educational DDoS Attack Simulator
    ====================================
    Components:
      1) Target Server
      2) Attacker Nodes
      3) GUI Dashboard
    """)

    choice = input("Start [server / attacker / gui / all]? ").strip().lower()

    if choice == "server":
        subprocess.run([sys.executable, "-m", "target_server.server"])
    elif choice == "attacker":
        subprocess.run([sys.executable, "-m", "attacker.traffic_generator"])
    elif choice == "gui":
        subprocess.run([sys.executable, "-m", "gui.dashboard"])
    elif choice == "all":
        subprocess.Popen([sys.executable, "-m", "target_server.server"])
        subprocess.Popen([sys.executable, "-m", "gui.dashboard"])
    else:
        print("Invalid choice. Use server / attacker / gui / all.")

if __name__ == "__main__":
    print(">>> run.py started")  # debug marker
    run()
