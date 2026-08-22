"""Simple multi-hour simulation demo."""
import yaml
from iotbuddy.core import IoTBuddy

with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)

buddy = IoTBuddy(cfg)
buddy.run_simulated(duration_min=10, seat_id="demo")
