from collections.abc import Generator
from dataclasses import asdict
from pathlib import Path

import pandas as pd

from log_analyzer.models import LogEntry
from log_analyzer.parser import parse_line


def load_data(path: str) -> tuple[pd.DataFrame, list[str]]:
    """
    Load log data from a file into a DataFrame and count malformed lines.

    Args:
        path (str): The path to the log file.
    Returns:
        tuple: A DataFrame containing valid log entries and a list of malformed lines.
    """
    rows = []
    malformed = []

    with Path(path).open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = parse_line(line)
            if entry:
                rows.append(entry)
            else:
                malformed.append(line)

    df = pd.DataFrame([asdict(e) for e in rows])
    # Parse timestamps upfront so later datetime subtractions in detect_bursts work
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df, malformed


def stream_entries(path: str) -> Generator[LogEntry | None, None, None]:
    """Generator variant of load_data:
    never builds a full DataFrame, so >32 GB files fit in memory

    Args:
        path (str): The path to the log file.
    Yields:
        Generator[LogEntry | None, None, None]: Parsed log entries, or None for malformed lines.
    """
    with Path(path).open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield parse_line(line)
