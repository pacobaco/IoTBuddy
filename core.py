from .eeg import extract_powers
from .state_machine import StateMachine
from .iot_bridge import IoTBridge
from .feedback import FeedbackEngine
import time
import numpy as np

class IoTBuddy:
    def __init__(self, mqtt_host="localhost", use_osc=True):
        self.sm = StateMachine()
        self.iot = IoTBridge(host=mqtt_host)
        self.feedback = FeedbackEngine(use_osc=use_osc)
        self.running = False

    def start(self):
        self.iot.connect()
        self.running = True
        print("IoT Buddy online – listening for state…")

    def process_window(self, eeg_window: np.ndarray, fs: float = 250.0):
        powers = extract_powers(eeg_window, fs)
        state = self.sm.update(powers)
        scene = self.sm.recommended_scene()

        self.iot.publish_state(state)
        self.iot.activate_scene(scene)
        self.feedback.update(state)

        return state, scene

    def run_simulated(self, duration_min=5):
        """Demo mode with synthetic EEG."""
        self.start()
        t0 = time.time()
        while time.time() - t0 < duration_min * 60 and self.running:
            # simple synthetic mixture
            t = np.linspace(0, 1, 250)
            signal = (0.4*np.sin(2*np.pi*6*t) +      # theta
                      0.3*np.sin(2*np.pi*10*t) +     # alpha
                      0.2*np.sin(2*np.pi*20*t) +     # beta
                      0.1*np.random.randn(250))
            state, scene = self.process_window(signal)
            print(f"[{state.primary.value:6}] conf={state.confidence:.2f} → {scene}")
            time.sleep(1.0)
