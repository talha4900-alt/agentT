import unittest
from agentt_seo.parser import PageParser, classify_links


class PageParserTests(unittest.TestCase):
    def test_extracts_basic_metadata_and_content(self):
        html = """<html><head><title> A useful page </title>
        <meta name="description" content="A page description">
        <meta name="robots" content="index,follow">
        <link rel="canonical" href="/guide"></head><body>
        <h1>Main heading</h1><h2>Section</h2>
        <img src="photo.jpg" alt="A product"><img src="missing-alt.jpg">
        <a href="/about">About</a><a href="https://other.example/">Other</a><a href="">Empty</a>
        </body></html>"""
        parser = PageParser("https://example.com/page")
        parser.feed(html)
        self.assertEqual(parser.title, "A useful page")
        self.assertEqual(parser.meta_description, "A page description")
        self.assertEqual(parser.robots, "index,follow")
        self.assertEqual(parser.canonical, "https://example.com/guide")
        self.assertEqual(parser.headings["h1"], ["Main heading"])
        self.assertEqual(parser.headings["h2"], ["Section"])
        self.assertEqual(len(parser.images), 2)
        self.assertFalse(parser.images[1]["has_alt"])
        self.assertEqual(parser.empty_href_count, 1)

    def test_classifies_links(self):
        self.assertEqual(classify_links("https://example.com/",
            ["https://example.com/about", "https://other.example/", "mailto:x@y.com"]), (1, 1))


if __name__ == "__main__":
    unittest.main()
