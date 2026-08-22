from pythonosc import udp_client
from .state_machine import CognitiveState


class FeedbackEngine:
    def __init__(self, use_osc: bool = True, ip: str = "127.0.0.1", port: int = 57120):
        self.use_osc = use_osc
        self.client = udp_client.SimpleUDPClient(ip, port) if use_osc else None

    def update(self, state: CognitiveState, seat_id: str = "default"):
        if not self.use_osc or self.client is None:
            return
        prefix = f"/buddy/{seat_id}"
        for band, power in state.powers.items():
            self.client.send_message(f"{prefix}/{band.value}", float(power))
        self.client.send_message(f"{prefix}/primary", state.primary.value)
        self.client.send_message(f"{prefix}/confidence", float(state.confidence))
