import pytest
import pandas as pd

from datetime import datetime, timedelta
from log_parser import LogEntry


@pytest.fixture
def sample_entries():
    base = datetime(2024, 1, 1, 12, 0, 0)
    return [
        LogEntry(
            str(base + timedelta(seconds=i * 30)),
            "ERROR",
            "192.168.1.1",
            "alice",
            "REQUEST",
            "timeout",
        )
        for i in range(8)  # 8 erreurs en < 5min → burst
    ]


@pytest.fixture
def sample_df(sample_entries):
    df = pd.DataFrame([vars(e) for e in sample_entries])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
