import re

from dataclasses import dataclass


@dataclass
class LogEntry:
    timestamp: str
    level: str
    ip: str
    user: str
    action: str
    message: str


def parse_line(line: str) -> LogEntry | None:
    """Parse a log line into a LogEntry object.

    Args:
        line (str): A single line from the log file.
    Returns:
        LogEntry | None: The parsed LogEntry object if the line matches the pattern, otherwise None.
    """
    pattern = r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] \[(.+?)\] \[(.+?)\] \[(.+?)\] (.+?): (.+)"
    match = re.match(pattern, line)
    if match:
        return LogEntry(*match.groups())
    return None
