"""Optional NeuroSync-style session helpers (lightweight)."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Session:
    session_id: str
    band: str
    duration_minutes: int
    started_at: datetime
    seat_ids: list[str]

    def is_active(self) -> bool:
        return datetime.utcnow() < self.started_at + timedelta(minutes=self.duration_minutes)
