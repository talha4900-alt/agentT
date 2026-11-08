import unittest
from unittest.mock import MagicMock, patch
from agentt_seo.auditor import audit_url, format_report


class AuditTests(unittest.TestCase):
    @patch("agentt_seo.auditor.urllib.request.urlopen")
    def test_audits_html_response(self, mock_urlopen):
        response = MagicMock()
        response.status = 200
        response.geturl.return_value = "https://example.com/"
        response.headers.get.return_value = "text/html; charset=utf-8"
        response.headers.get_content_charset.return_value = "utf-8"
        response.read.return_value = (
            b"<html><head><title>A sufficiently descriptive example page title</title>"
            b'<meta name="description" content="A useful description for this example page.">'
            b'<link rel="canonical" href="https://example.com/"></head>'
            b"<body><h1>Example</h1><img src='a.jpg' alt='Example'></body></html>")
        mock_urlopen.return_value.__enter__.return_value = response
        report = audit_url("example.com")
        self.assertEqual(report["http_status"], 200)
        self.assertEqual(report["page"]["title"], "A sufficiently descriptive example page title")
        self.assertEqual(report["summary"]["total"], 9)
        self.assertIn("agentT SEO Auditor", format_report(report))

    def test_rejects_empty_url(self):
        with self.assertRaises(ValueError):
            audit_url("   ")


if __name__ == "__main__":
    unittest.main()
