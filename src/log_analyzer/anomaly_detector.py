from collections import deque
from datetime import datetime


def detect_bursts(df, window=300, threshold=5):
    """
    Detects bursts of errors for each user in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing log data.
        window (int): The time window in seconds to consider for bursts.
        threshold (int): The number of errors that constitutes a burst.

    Returns:
        pd.DataFrame: A DataFrame containing users with bursts of errors.
    """

    def has_burst(group):
        """
        Checks if a group of log entries contains a burst of errors.

        Args:
            group (pd.DataFrame): A DataFrame containing log entries for a specific (ip, user) pair.
        Returns:
            bool: True if a burst is detected, False otherwise.
        """
        times = sorted(group["timestamp"])
        window_q = deque()

        for t in times:
            window_q.append(t)
            # Sliding window: drop errors older than `window` seconds so the deque only
            # holds the current interval
            while (t - window_q[0]).total_seconds() > window:
                window_q.popleft()
            # Strictly greater: spec flags "more than" threshold errors
            # (6+ with the default of 5)
            if len(window_q) > threshold:
                return True
        return False

    result = df[df["level"] == "ERROR"].groupby(["ip", "user"]).filter(has_burst)
    return result.groupby(["ip", "user"])


def detect_bursts_from_timestamps(
    error_timestamps: dict[tuple, list[datetime]], window: int = 300, threshold: int = 5
) -> list[dict]:
    """
    Streaming alternative to detect_bursts: runs on accumulated timestamps, no DataFrame available
    Detects bursts of errors from a dictionary of error timestamps.

    Args:
        error_timestamps (dict[tuple, list[datetime]]): keys are (ip, user) pairs,
        values are lists of parsed error timestamps.
        window (int): The time window in seconds to consider for bursts.
        threshold (int): The number of errors that constitutes a burst.

    Returns:
        list[dict]: suspicious (ip, user) pairs with bursts of errors.
    """
    suspicious = []

    for (ip, user), timestamps in error_timestamps.items():
        parsed = sorted(timestamps)
        window_q: deque[datetime] = deque()

        for t in parsed:
            window_q.append(t)
            while (t - window_q[0]).total_seconds() > window:
                window_q.popleft()

            if len(window_q) > threshold:
                suspicious.append(
                    {
                        "ip": ip,
                        "user": user,
                        "error_count": len(parsed),
                        "time_range": (str(parsed[0]), str(parsed[-1])),
                    }
                )
                break  # detected burst, no need to continue for this pair

    return suspicious
