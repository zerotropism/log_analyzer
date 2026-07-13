import pandas as pd

from typing import Iterable
from log_parser import LogEntry
from collections import defaultdict
from queries import successful_logins_per_user, ips_per_user
from anomaly_detector import detect_bursts, detect_bursts_from_timestamps


def generate_report(df: pd.DataFrame, malformed_count: int = 0) -> dict:
    """
    Generates a report containing various statistics from the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing log data.
    Returns:
        dict: A dictionary containing the report sections.
    """
    bursts = detect_bursts(df)

    return {
        "summary": {
            "total_entries": len(df),
            "total_users": df["user"].nunique(),
            "total_ips": df["ip"].nunique(),
            "malformed_entries": malformed_count,
        },
        "suspicious_activity": [
            {
                "ip": ip,
                "user": user,
                "error_count": len(group),
                "time_range": (group["timestamp"].min(), group["timestamp"].max()),
            }
            for (ip, user), group in bursts
        ],
        "logins_per_user": successful_logins_per_user(df),
        "ips_per_user": ips_per_user(df),
    }


def generate_report_from_entries(entries: Iterable[LogEntry | None]) -> dict:
    malformed_count = 0
    total = 0
    users = set()
    ips = set()
    logins_per_user = defaultdict(int)
    ips_per_user_map = defaultdict(set)
    error_timestamps: dict[tuple, list] = defaultdict(list)

    for entry in entries:
        if entry is None:
            malformed_count += 1
            continue

        total += 1
        users.add(entry.user)
        ips.add(entry.ip)
        ips_per_user_map[entry.user].add(entry.ip)

        if entry.action == "LOGIN" and entry.level == "INFO":
            logins_per_user[entry.user] += 1

        if entry.level == "ERROR":
            error_timestamps[(entry.ip, entry.user)].append(entry.timestamp)

    suspicious = detect_bursts_from_timestamps(error_timestamps)

    return {
        "summary": {
            "total_entries": total,
            "total_users": len(users),
            "total_ips": len(ips),
            "malformed_entries": malformed_count,
        },
        "suspicious_activity": suspicious,
        "logins_per_user": dict(logins_per_user),
        "ips_per_user": {u: list(i) for u, i in ips_per_user_map.items()},
    }
