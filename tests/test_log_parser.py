import pytest

from log_parser import parse_line, LogEntry

VALID_LINE = "[2024-01-01 12:00:00] [ERROR] [192.168.1.1] [alice] LOGIN: failed attempt"


@pytest.mark.parametrize(
    "line,expected",
    [
        (
            VALID_LINE,
            LogEntry(
                "2024-01-01 12:00:00",
                "ERROR",
                "192.168.1.1",
                "alice",
                "LOGIN",
                "failed attempt",
            ),
        ),
        ("", None),
        ("garbage", None),
        (
            "[2024-01-01 12:00:00] [INFO] [10.0.0.1] [bob] LOGIN: success",
            LogEntry(
                "2024-01-01 12:00:00", "INFO", "10.0.0.1", "bob", "LOGIN", "success"
            ),
        ),
    ],
)
def test_parse_line(line, expected):
    assert parse_line(line) == expected
