from datetime import datetime

from log_analyzer.models import LogEntry
from log_analyzer.report import generate_report_from_entries


def test_generate_report_from_entries_counts_malformed():
    entries = [
        None,
        None,
        LogEntry(datetime(2024, 1, 1, 12, 0), "INFO", "1.2.3.4", "alice", "LOGIN", "ok"),
    ]
    report = generate_report_from_entries(iter(entries))
    assert report["summary"]["malformed_entries"] == 2
    assert report["summary"]["total_entries"] == 1


def test_generate_report_counts_logins():
    entries = [
        LogEntry(datetime(2024, 1, 1, 12, 0), "INFO", "1.2.3.4", "alice", "LOGIN", "ok"),
        LogEntry(datetime(2024, 1, 1, 12, 1), "INFO", "1.2.3.4", "alice", "LOGIN", "ok"),
        LogEntry(datetime(2024, 1, 1, 12, 2), "ERROR", "1.2.3.4", "alice", "REQUEST", "fail"),
    ]
    report = generate_report_from_entries(iter(entries))
    assert report["logins_per_user"]["alice"] == 2
