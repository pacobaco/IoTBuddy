import time
import numpy as np
from .eeg import extract_powers
from .iot_bridge import IoTBridge
from .feedback import FeedbackEngine
from .multi_seat.seat_manager import SeatManager
from .multi_seat.arbitrator import Arbitrator


class IoTBuddy:
    def __init__(self, config: dict):
        mqtt_cfg = config.get("mqtt", {})
        self.iot = IoTBridge(
            host=mqtt_cfg.get("host", "localhost"),
            port=mqtt_cfg.get("port", 1883),
            username=mqtt_cfg.get("username"),
            password=mqtt_cfg.get("password"),
            base_topic=mqtt_cfg.get("base_topic", "iotbuddy"),
        )
        ms_cfg = config.get("multi_seat", {})
        self.seat_manager = SeatManager(
            timeout_seconds=ms_cfg.get("seat_timeout_seconds", 90)
        )
        self.arbitrator = Arbitrator(
            night_start=ms_cfg.get("night_start_hour", 22),
            night_end=ms_cfg.get("night_end_hour", 7),
        )
        fb_cfg = config.get("feedback", {})
        self.feedback = FeedbackEngine(
            use_osc=fb_cfg.get("osc_enabled", True),
            ip=fb_cfg.get("osc_ip", "127.0.0.1"),
            port=fb_cfg.get("osc_port", 57120),
        )
        self.running = False

    def start(self):
        try:
            self.iot.connect()
        except Exception as e:
            print(f"MQTT connection warning: {e}")
        self.running = True
        print("IoT Buddy online")

    def process_seat_window(
        self, seat_id: str, eeg_window: np.ndarray, fs: float = 250.0
    ):
        seat = self.seat_manager.get(seat_id) or self.seat_manager.register(seat_id)
        powers = extract_powers(eeg_window, fs)
        state = seat.update(powers)
        scene_req = seat.requested_scene()

        self.iot.publish_state(seat_id, state, scene_req)
        final_scene = self.arbitrator.decide(self.seat_manager.active_seats())
        self.iot.activate_scene(final_scene)
        self.feedback.update(state, seat_id=seat_id)

        return state, final_scene

    def run_simulated(self, duration_min: int = 5, seat_id: str = "default"):
        self.start()
        self.seat_manager.register(seat_id, name="Simulator")
        t0 = time.time()
        while time.time() - t0 < duration_min * 60 and self.running:
            t = np.linspace(0, 1, 250)
            signal = (
                0.35 * np.sin(2 * np.pi * 6 * t)
                + 0.30 * np.sin(2 * np.pi * 10 * t)
                + 0.20 * np.sin(2 * np.pi * 20 * t)
                + 0.15 * np.random.randn(250)
            )
            state, scene = self.process_seat_window(seat_id, signal)
            print(
                f"[{seat_id}] {state.primary.value:6} "
                f"conf={state.confidence:.2f} → {scene}"
            )
            time.sleep(1.0)
