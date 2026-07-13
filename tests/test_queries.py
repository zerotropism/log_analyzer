import pandas as pd
import pytest
from queries import successful_logins_per_user, ips_per_user, filter_entries


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        [
            {
                "timestamp": "2024-01-01 12:00:00",
                "level": "INFO",
                "ip": "192.168.1.1",
                "user": "alice",
                "action": "LOGIN",
                "message": "ok",
            },
            {
                "timestamp": "2024-01-01 12:01:00",
                "level": "INFO",
                "ip": "192.168.1.1",
                "user": "alice",
                "action": "LOGIN",
                "message": "ok",
            },
            {
                "timestamp": "2024-01-01 12:02:00",
                "level": "ERROR",
                "ip": "192.168.1.2",
                "user": "alice",
                "action": "LOGIN",
                "message": "fail",
            },
            {
                "timestamp": "2024-01-01 12:03:00",
                "level": "INFO",
                "ip": "10.0.0.1",
                "user": "bob",
                "action": "LOGOUT",
                "message": "ok",
            },
            {
                "timestamp": "2024-01-01 12:04:00",
                "level": "INFO",
                "ip": "10.0.0.2",
                "user": "bob",
                "action": "LOGIN",
                "message": "ok",
            },
        ]
    )


def test_successful_logins_per_user(sample_df):
    result = successful_logins_per_user(sample_df)
    assert result["alice"] == 2
    assert result["bob"] == 1


def test_successful_logins_excludes_errors(sample_df):
    result = successful_logins_per_user(sample_df)
    # la ligne ERROR de alice ne doit pas être comptée
    assert result["alice"] == 2


def test_ips_per_user(sample_df):
    result = ips_per_user(sample_df)
    assert set(result["alice"]) == {"192.168.1.1", "192.168.1.2"}
    assert set(result["bob"]) == {"10.0.0.1", "10.0.0.2"}


def test_filter_entries_by_user(sample_df):
    result = filter_entries(sample_df, user="alice")
    assert len(result) == 3
    assert all(result["user"] == "alice")


def test_filter_entries_by_level_and_action(sample_df):
    result = filter_entries(sample_df, level="INFO", action="LOGIN")
    assert len(result) == 3


def test_filter_entries_no_match(sample_df):
    result = filter_entries(sample_df, user="unknown")
    assert len(result) == 0
