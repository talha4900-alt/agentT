# agentT SEO Auditor

A small, open-source command-line tool that fetches a public web page and reports practical on-page SEO checks. It is designed for developers, independent website owners, and small businesses that want a readable first-pass audit without a paid SEO platform.

> **Project status:** Early development. The first version audits one URL at a time. It is not a full-site crawler, a Google ranking predictor, or a substitute for a professional technical SEO review.

## What it checks

- HTTP response status and final URL after redirects
- HTML page title and its character count
- Meta description and its character count
- Canonical link
- H1 presence and count
- Heading structure (H1-H6)
- Images missing an `alt` attribute
- Internal and external link counts
- Links with empty or missing `href`
- Basic robots meta directives

The tool reports observations and simple heuristics. Recommended title and description lengths are guidelines, not Google ranking rules.

## Requirements

- Python 3.10 or newer
- No third-party Python dependencies

## Install

```bash
git clone https://github.com/talha4900-alt/agentT.git
cd agentT
```

Run directly from the repository:

```bash
python -m agentt_seo https://example.com
```

On Windows, use `py` if `python` is not available:

```powershell
py -m agentt_seo https://example.com
```

## Usage

Human-readable report:

```bash
python -m agentt_seo https://example.com
```

JSON output:

```bash
python -m agentt_seo https://example.com --json
```

Set a request timeout:

```bash
python -m agentt_seo https://example.com --timeout 20
```

The command exits with status code `1` if the page could not be fetched, and `0` when an audit report is produced.

## Development and tests

```bash
python -m unittest discover -s tests -v
```

No live website is required for the tests.

## Responsible use

Only audit websites you are allowed to access. The tool makes a single page request, follows normal HTTP redirects, and does not attempt to bypass authentication, robots restrictions, rate limits, or other access controls. Be considerate when auditing websites you do not own.

See [docs/scope-and-limitations.md](docs/scope-and-limitations.md) and [docs/roadmap.md](docs/roadmap.md).

## Contributing

Bug reports, focused improvements, tests, and documentation contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the MIT License. See [LICENSE](LICENSE).

---

Built by [Talha Ismail](https://github.com/talha4900-alt). The project is informed by hands-on work with small-business websites and e-commerce, including WordPress and WooCommerce. It is an independent community project and is not affiliated with Google or any search engine.
