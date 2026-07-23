# Log Analyzer

A Python security log analysis tool. It parses server log files to detect suspicious behavior, extract usage statistics, and generate JSON reports.

## Features

- **Log parsing**: reads and validates the format `[TIMESTAMP] [LEVEL] [IP] [USER] ACTION: message`
- **Anomaly detection**: identifies sources (IP/user) generating more than 5 errors within a 5-minute window
- **Queries**:
  - Number of successful logins per user
  - List of IP addresses per user
- **JSON report**: global summary + suspicious activity + login statistics
- **Streaming mode**: line-by-line processing for large files (> 32 GB)
- **Robustness**: malformed lines are counted without interrupting the analysis

## Expected Log Format

```
[2024-01-15 10:23:45] [INFO] [192.168.1.100] [john_doe] LOGIN: Successful login attempt
[2024-01-15 10:23:47] [ERROR] [192.168.1.101] [jane_smith] ACCESS: Invalid permission for /admin/users
```

## Installation

Requires Python 3.12+.

```bash
pip install -e .
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Usage

```bash
# Standard analysis
python main.py --input input/server_activity.log

# Save the report to a file
python main.py --input input/server_activity.log --output report.json

# Streaming mode for large files (> 32 GB)
python main.py --input input/server_activity.log --large-file
```

## Output Report Structure

```json
{
  "summary": {
    "total_entries": 1500,
    "total_users": 12,
    "total_ips": 8,
    "malformed_entries": 3
  },
  "suspicious_activity": [
    {
      "ip": "192.168.1.101",
      "user": "jane_smith",
      "error_count": 7,
      "time_range": ["2024-01-15 10:20:00", "2024-01-15 10:24:30"]
    }
  ],
  "logins_per_user": {
    "john_doe": 5
  },
  "ips_per_user": {
    "john_doe": ["192.168.1.100", "10.0.0.5"]
  }
}
```

## Project Structure

```
log_analyzer/
├── main.py               # CLI entry point
├── log_loader.py         # File loading (DataFrame or streaming mode)
├── log_parser.py         # Log line parsing
├── anomaly_detector.py   # Error burst detection
├── queries.py            # Analytical queries (logins, IPs)
├── report.py             # JSON report generation
├── input/                # Sample log files
└── tests/                # Unit tests (pytest)
```

## Tests

```bash
pytest
```

## Dependencies

| Package   | Role                            |
|-----------|---------------------------------|
| `pandas`  | Log data manipulation           |
| `pytest`  | Unit testing                    |