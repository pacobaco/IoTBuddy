from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict
from ..state_machine import StateMachine, CognitiveState


@dataclass
class Seat:
    seat_id: str
    name: str = ""
    priority: int = 1
    private_audio: bool = True
    sm: StateMachine = field(default_factory=StateMachine)
    last_seen: datetime = field(default_factory=datetime.utcnow)

    def update(self, powers: Dict[str, float]) -> CognitiveState:
        self.last_seen = datetime.utcnow()
        return self.sm.update(powers)

    def requested_scene(self) -> str:
        return self.sm.recommended_scene()
