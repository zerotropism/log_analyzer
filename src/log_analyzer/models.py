"""Domain models. LogEntry stays a dataclass: it is built once per log line."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class LogEntry:
    timestamp: datetime
    level: str
    ip: str
    user: str
    action: str
    message: str
