from report import generate_report_from_entries
from log_parser import LogEntry


def test_generate_report_from_entries_counts_malformed():
    entries = [
        None,
        None,
        LogEntry("2024-01-01 12:00:00", "INFO", "1.2.3.4", "alice", "LOGIN", "ok"),
    ]
    report = generate_report_from_entries(iter(entries))
    assert report["summary"]["malformed_entries"] == 2
    assert report["summary"]["total_entries"] == 1


def test_generate_report_counts_logins():
    entries = [
        LogEntry("2024-01-01 12:00:00", "INFO", "1.2.3.4", "alice", "LOGIN", "ok"),
        LogEntry("2024-01-01 12:01:00", "INFO", "1.2.3.4", "alice", "LOGIN", "ok"),
        LogEntry("2024-01-01 12:02:00", "ERROR", "1.2.3.4", "alice", "REQUEST", "fail"),
    ]
    report = generate_report_from_entries(iter(entries))
    assert report["logins_per_user"]["alice"] == 2
