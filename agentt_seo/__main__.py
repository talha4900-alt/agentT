"""Command-line entry point."""
import argparse
import http.client
import sys
import urllib.error
from .auditor import audit_url, format_report, report_json


def main():
    parser = argparse.ArgumentParser(
        prog="agentt-seo",
        description="Run a lightweight on-page SEO audit for one public URL.")
    parser.add_argument("url", help="Website URL (https:// is added when omitted)")
    parser.add_argument("--json", action="store_true", help="Print report as JSON")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout in seconds")
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be at least 1 second")
    try:
        report = audit_url(args.url, timeout=args.timeout)
    except (ValueError, http.client.HTTPException, urllib.error.URLError,
            TimeoutError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(report_json(report) if args.json else format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
