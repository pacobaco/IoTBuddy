from datetime import datetime
from typing import Dict
from .seat import Seat
from ..state_machine import Band


class Arbitrator:
    def __init__(self, night_start: int = 22, night_end: int = 7):
        self.night_start = night_start
        self.night_end = night_end

    def decide(self, active_seats: Dict[str, Seat]) -> str:
        if not active_seats:
            return "buddy_neutral"

        hour = datetime.now().hour
        is_night = hour >= self.night_start or hour < self.night_end

        if is_night:
            for seat in active_seats.values():
                st = seat.sm.current
                if st and st.primary == Band.DELTA and st.confidence > 0.55:
                    return "buddy_delta"

        scores: Dict[str, float] = {}
        for seat in active_seats.values():
            scene = seat.requested_scene()
            conf = seat.sm.current.confidence if seat.sm.current else 0.5
            scores[scene] = scores.get(scene, 0.0) + seat.priority * conf

        return max(scores, key=scores.get) if scores else "buddy_neutral"
