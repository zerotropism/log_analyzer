from anomaly_detector import detect_bursts_from_timestamps
from datetime import datetime, timedelta


def make_timestamps(n, gap_seconds=30):
    base = datetime(2024, 1, 1, 12, 0, 0)
    return [str(base + timedelta(seconds=i * gap_seconds)) for i in range(n)]


def test_burst_detected_above_threshold():
    data = {("192.168.1.1", "alice"): make_timestamps(8, gap_seconds=20)}
    result = detect_bursts_from_timestamps(data, window=300, threshold=5)
    assert len(result) == 1
    assert result[0]["user"] == "alice"


def test_no_burst_below_threshold():
    data = {("10.0.0.1", "bob"): make_timestamps(4, gap_seconds=20)}
    result = detect_bursts_from_timestamps(data, window=300, threshold=5)
    assert result == []


def test_burst_not_detected_when_spread_out():
    # erreurs espacées de 2min → hors fenêtre de 5min
    data = {("10.0.0.1", "bob"): make_timestamps(8, gap_seconds=120)}
    result = detect_bursts_from_timestamps(data, window=300, threshold=5)
    assert result == []
