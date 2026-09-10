from dataclasses import asdict
from datetime import datetime, timedelta

import pandas as pd
import pytest

from log_analyzer.models import LogEntry


@pytest.fixture
def sample_entries():
    base = datetime(2024, 1, 1, 12, 0, 0)
    return [
        LogEntry(
            base + timedelta(seconds=i * 30),
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
    df = pd.DataFrame([asdict(e) for e in sample_entries])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
