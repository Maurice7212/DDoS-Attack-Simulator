"""
Traffic generator entry point for launching attacks.
"""

from attacker.attacks import run_attack, stop_attacks
import yaml

CONFIG = "attacker/config.yaml"

def main():
    with open(CONFIG) as f:
        cfg = yaml.safe_load(f)

    run_attack(
        target=cfg.get("target", "http://127.0.0.1:5000"),
        attack_type=cfg.get("attack_type", "http"),
        rps=cfg.get("requests_per_second", 10),
        duration=cfg.get("duration_seconds", 30),
        num_nodes=cfg.get("num_nodes", 1),
    )

if __name__ == "__main__":
    main()
