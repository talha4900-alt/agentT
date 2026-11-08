"""Fetch and audit a single public web page."""
from __future__ import annotations
import json
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any
from .parser import PageParser, classify_links

USER_AGENT = "agentT-SEO-Auditor/0.1 (+https://github.com/talha4900-alt/agentT)"
MAX_RESPONSE_BYTES = 2_000_000


@dataclass
class Check:
    name: str
    status: str
    message: str
    value: Any = None


def _check(name, condition, success, warning, value=None):
    return Check(name, "pass" if condition else "warning",
                 success if condition else warning, value)


def audit_url(url: str, timeout: int = 15) -> dict[str, Any]:
    """Fetch one URL and return an on-page SEO report."""
    request_url = url.strip()
    if not request_url:
        raise ValueError("URL cannot be empty.")
    if not request_url.startswith(("http://", "https://")):
        request_url = "https://" + request_url
    request = urllib.request.Request(
        request_url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status_code = response.status
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        status_code = exc.code
        final_url = exc.geturl()
        content_type = exc.headers.get("Content-Type", "") if exc.headers else ""
        charset = exc.headers.get_content_charset() if exc.headers else None
        body = exc.read(MAX_RESPONSE_BYTES + 1)
    body = body[:MAX_RESPONSE_BYTES]
    if "html" not in content_type.lower() and content_type:
        raise ValueError(f"The URL did not return HTML (Content-Type: {content_type}).")
    html = body.decode(charset or "utf-8", errors="replace")
    page = PageParser(final_url)
    page.feed(html)
    page.close()
    internal_links, external_links = classify_links(final_url, page.links)
    h1_count = len(page.headings["h1"])
    missing_alt = sum(1 for item in page.images if not item["has_alt"])
    title_length = len(page.title)
    description_length = len(page.meta_description)
    checks = [
        _check("HTTP response", 200 <= status_code < 400,
               f"Page returned HTTP {status_code}.", f"Page returned HTTP {status_code}.", status_code),
        _check("Page title", bool(page.title), "A page title is present.", "The page title is missing.", page.title),
        _check("Title length", 30 <= title_length <= 60,
               f"Title is {title_length} characters (30-60 is a common guideline).",
               f"Title is {title_length} characters; review whether it is descriptive and concise.", title_length),
        _check("Meta description", bool(page.meta_description),
               "A meta description is present.", "The meta description is missing.", page.meta_description),
        _check("Description length", 70 <= description_length <= 160,
               f"Description is {description_length} characters (70-160 is a common guideline).",
               f"Description is {description_length} characters; review its clarity and length.", description_length),
        _check("Canonical URL", bool(page.canonical),
               "A canonical link is present.", "No canonical link was found.", page.canonical),
        _check("H1 heading", h1_count == 1, "Exactly one H1 heading was found.",
               f"Found {h1_count} H1 headings; review the page's main heading.", h1_count),
        _check("Image alt text", missing_alt == 0,
               "All detected images have an alt attribute.",
               f"{missing_alt} of {len(page.images)} detected images are missing an alt attribute.",
               {"total": len(page.images), "missing_alt": missing_alt}),
        _check("Robots meta", "noindex" not in page.robots.lower(),
               "No noindex directive was found in the robots meta tag.",
               "A noindex directive was found in the robots meta tag.", page.robots),
    ]
    return {
        "tool": "agentT SEO Auditor", "version": "0.1.0",
        "requested_url": request_url, "final_url": final_url,
        "http_status": status_code, "content_type": content_type,
        "page": {
            "title": page.title, "title_length": title_length,
            "meta_description": page.meta_description, "description_length": description_length,
            "canonical": page.canonical, "robots": page.robots, "headings": page.headings,
            "images": page.images,
            "links": {"internal": internal_links, "external": external_links,
                      "empty_or_missing_href": page.empty_href_count},
        },
        "checks": [asdict(item) for item in checks],
        "summary": {"total": len(checks),
                    "passed": sum(item.status == "pass" for item in checks),
                    "warnings": sum(item.status == "warning" for item in checks)},
    }


def format_report(report):
    lines = ["agentT SEO Auditor", f"URL: {report['final_url']}",
             f"HTTP status: {report['http_status']}", ""]
    for item in report["checks"]:
        lines.append(f"{'PASS' if item['status'] == 'pass' else 'WARN':4}  "
                     f"{item['name']}: {item['message']}")
    summary = report["summary"]
    lines.extend(["", f"Summary: {summary['total']} checks, {summary['passed']} passed, "
                       f"{summary['warnings']} warnings"])
    return "\n".join(lines)


def report_json(report):
    return json.dumps(report, indent=2, ensure_ascii=False)
