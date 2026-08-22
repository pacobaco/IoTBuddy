from typing import Dict, Optional
from datetime import datetime, timedelta
from .seat import Seat


class SeatManager:
    def __init__(self, timeout_seconds: int = 90):
        self.seats: Dict[str, Seat] = {}
        self.timeout = timedelta(seconds=timeout_seconds)

    def register(self, seat_id: str, name: str = "", priority: int = 1) -> Seat:
        if seat_id not in self.seats:
            self.seats[seat_id] = Seat(seat_id=seat_id, name=name, priority=priority)
        else:
            seat = self.seats[seat_id]
            seat.name = name or seat.name
            seat.priority = priority
        self.seats[seat_id].last_seen = datetime.utcnow()
        return self.seats[seat_id]

    def heartbeat(self, seat_id: str):
        if seat_id in self.seats:
            self.seats[seat_id].last_seen = datetime.utcnow()

    def get(self, seat_id: str) -> Optional[Seat]:
        return self.seats.get(seat_id)

    def active_seats(self) -> Dict[str, Seat]:
        now = datetime.utcnow()
        return {
            sid: s for sid, s in self.seats.items()
            if now - s.last_seen < self.timeout
        }

    def remove_stale(self):
        self.seats = self.active_seats()
