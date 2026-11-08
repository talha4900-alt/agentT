"""Small HTML parser used by the agentT SEO auditor."""
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse


class PageParser(HTMLParser):
    """Extract common on-page SEO elements from an HTML document."""

    def __init__(self, page_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.title_parts = []
        self.title = ""
        self.meta_description = ""
        self.robots = ""
        self.canonical = ""
        self.headings = {f"h{i}": [] for i in range(1, 7)}
        self.images = []
        self.links = []
        self.empty_href_count = 0
        self._in_title = False
        self._heading_tag = None
        self._heading_parts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").strip().lower()
            if name == "description" and not self.meta_description:
                self.meta_description = attrs_dict.get("content", "").strip()
            elif name == "robots" and not self.robots:
                self.robots = attrs_dict.get("content", "").strip()
        elif tag == "link":
            rel = {part.lower() for part in attrs_dict.get("rel", "").split()}
            if "canonical" in rel and not self.canonical:
                self.canonical = urljoin(self.page_url, attrs_dict.get("href", "").strip())
        elif tag in self.headings:
            self._heading_tag = tag
            self._heading_parts = []
        elif tag == "img":
            self.images.append({"src": attrs_dict.get("src", ""),
                                "has_alt": "alt" in attrs_dict,
                                "alt": attrs_dict.get("alt", "")})
        elif tag == "a":
            href = attrs_dict.get("href", "").strip()
            if href:
                self.links.append(urljoin(self.page_url, href))
            else:
                self.empty_href_count += 1

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
            self.title = " ".join("".join(self.title_parts).split())
        elif tag == self._heading_tag:
            if self._heading_tag:
                text = " ".join("".join(self._heading_parts).split())
                self.headings[self._heading_tag].append(text)
            self._heading_tag = None
            self._heading_parts = []

    def handle_data(self, data):
        if self._in_title:
            self.title_parts.append(data)
        if self._heading_tag:
            self._heading_parts.append(data)


def classify_links(page_url: str, links: list[str]) -> tuple[int, int]:
    """Return (internal, external) counts, ignoring non-web schemes."""
    base = urlparse(page_url)
    internal = external = 0
    for link in links:
        parsed = urlparse(link)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            continue
        if parsed.netloc.lower() == base.netloc.lower():
            internal += 1
        else:
            external += 1
    return internal, external
