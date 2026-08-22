import paho.mqtt.client as mqtt
import json
from typing import Optional

class IoTBridge:
    def __init__(self, host="localhost", port=1883, base_topic="iotbuddy"):
        self.client = mqtt.Client()
        self.base = base_topic
        self.host = host
        self.port = port
        self.connected = False

    def connect(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()
        self.connected = True

    def publish_state(self, state):
        payload = {
            "primary": state.primary.value,
            "confidence": round(state.confidence, 3),
            "powers": {k.value: round(v, 4) for k, v in state.powers.items()},
            "scene": None  # filled by caller
        }
        self.client.publish(f"{self.base}/state", json.dumps(payload), qos=1)

    def activate_scene(self, scene_name: str):
        # Home Assistant compatible
        self.client.publish(
            "homeassistant/scene/activate",
            json.dumps({"entity_id": f"scene.{scene_name}"}),
            qos=1
        )
        self.client.publish(f"{self.base}/scene", scene_name, qos=1)
