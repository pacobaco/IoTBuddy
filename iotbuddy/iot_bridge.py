import json
import paho.mqtt.client as mqtt
from typing import Optional


class IoTBridge:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_topic: str = "iotbuddy",
    ):
        self.client = mqtt.Client()
        if username:
            self.client.username_pw_set(username, password)
        self.host = host
        self.port = port
        self.base = base_topic
        self.connected = False

    def connect(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()
        self.connected = True

    def publish_state(self, seat_id: str, state, scene_request: str):
        payload = {
            "primary": state.primary.value,
            "confidence": round(state.confidence, 3),
            "powers": {k.value: round(v, 4) for k, v in state.powers.items()},
            "scene_request": scene_request,
        }
        self.client.publish(
            f"{self.base}/seat/{seat_id}/state",
            json.dumps(payload),
            qos=1,
        )

    def activate_scene(self, scene_name: str):
        self.client.publish(
            "homeassistant/scene/activate",
            json.dumps({"entity_id": f"scene.{scene_name}"}),
            qos=1,
        )
        self.client.publish(
            f"{self.base}/arbitrator/final_scene",
            scene_name,
            qos=1,
        )
