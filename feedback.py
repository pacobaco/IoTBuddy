from pythonosc import udp_client
from .state_machine import Band

class FeedbackEngine:
    def __init__(self, use_osc=True, ip="127.0.0.1", port=57120):
        self.use_osc = use_osc
        if use_osc:
            self.client = udp_client.SimpleUDPClient(ip, port)

    def update(self, state):
        if not self.use_osc:
            return
        # Send powers + primary band (neuroclash style)
        for band, power in state.powers.items():
            self.client.send_message(f"/buddy/{band.value}", float(power))
        self.client.send_message("/buddy/primary", state.primary.value)
        self.client.send_message("/buddy/confidence", float(state.confidence))
