from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List


class Band(str, Enum):
    DELTA = "delta"
    THETA = "theta"
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"


@dataclass
class CognitiveState:
    primary: Band
    confidence: float
    powers: Dict[Band, float]
    timestamp: datetime = field(default_factory=datetime.utcnow)


class StateMachine:
    def __init__(self):
        self.history: List[CognitiveState] = []
        self.current: Optional[CognitiveState] = None
        self.mode_lock: Optional[Band] = None

    def update(self, powers: Dict[str, float]) -> CognitiveState:
        vals = {
            Band(k.lower()): float(v)
            for k, v in powers.items()
            if k.lower() in Band._value2member_map_
        }
        total = sum(vals.values()) + 1e-9
        norm = {b: v / total for b, v in vals.items()}
        primary = max(norm, key=norm.get)
        state = CognitiveState(
            primary=primary,
            confidence=norm[primary],
            powers=norm,
        )
        self.history.append(state)
        if len(self.history) > 3600:
            self.history = self.history[-3600:]
        self.current = state
        return state

    def recommended_scene(self) -> str:
        if self.mode_lock:
            return f"buddy_{self.mode_lock.value}"
        if not self.current:
            return "buddy_neutral"

        band = self.current.primary
        hour = datetime.now().hour

        if 0 <= hour < 6 or (band == Band.DELTA and self.current.confidence > 0.6):
            return "buddy_delta"
        if band in (Band.THETA, Band.ALPHA) and hour >= 20:
            return "buddy_winddown"
        if band == Band.BETA:
            return "buddy_focus"
        if band == Band.GAMMA:
            return "buddy_peak"
        return f"buddy_{band.value}"

    def lock(self, band: Band):
        self.mode_lock = band

    def unlock(self):
        self.mode_lock = None
