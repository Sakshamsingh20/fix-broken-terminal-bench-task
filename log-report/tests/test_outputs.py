import json
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")


def _expected_stats():
    """Independently recompute the expected report directly from the log."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    top_path, top_count = paths.most_common(1)[0]
    tied_top_paths = {p for p, c in paths.items() if c == top_count}
    return total, len(ips), tied_top_paths


def test_report_exists_and_valid_json():
    """Success criterion 1: /app/report.json exists and contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    with open(REPORT_PATH) as f:
        json.load(f)  # raises if not valid JSON


def test_total_requests():
    """Success criterion 2: total_requests matches the non-blank line count."""
    expected_total, _, _ = _expected_stats()
    report = json.load(open(REPORT_PATH))
    assert report.get("total_requests") == expected_total, (
        f"expected total_requests={expected_total}, got {report.get('total_requests')}"
    )


def test_unique_ips():
    """Success criterion 3: unique_ips matches the distinct client IP count."""
    _, expected_unique_ips, _ = _expected_stats()
    report = json.load(open(REPORT_PATH))
    assert report.get("unique_ips") == expected_unique_ips, (
        f"expected unique_ips={expected_unique_ips}, got {report.get('unique_ips')}"
    )


def test_top_path():
    """Success criterion 4: top_path matches the most frequently requested path."""
    _, _, expected_top_paths = _expected_stats()
    report = json.load(open(REPORT_PATH))
    assert report.get("top_path") in expected_top_paths, (
        f"expected top_path to be one of {expected_top_paths}, got {report.get('top_path')}"
    )
