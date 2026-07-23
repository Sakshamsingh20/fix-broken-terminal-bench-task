There's an Apache-style access log at /app/access.log. Parse it and write a JSON
summary report to /app/report.json.

The report must be a single JSON object with exactly these three keys:

- total_requests: integer, the number of non-blank lines in the log (one line = one request).
- unique_ips: integer, the number of distinct client IP addresses that appear in the log (the first whitespace-delimited field of each line).
- top_path: string, the request path (e.g. "/index.html") that occurs most often across all requests in the log. If there is a tie, any one of the tied paths is acceptable.

Success criteria:

1. /app/report.json exists and contains valid JSON.
2. The JSON object's total_requests field exactly matches the number of non-blank lines in /app/access.log.
3. The JSON object's unique_ips field exactly matches the number of distinct client IPs in /app/access.log.
4. The JSON object's top_path field matches the most frequently requested path in /app/access.log.
