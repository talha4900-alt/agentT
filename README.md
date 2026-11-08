# agentT SEO Auditor

**Free and open-source SEO auditing for everyone.**

agentT SEO Auditor is a lightweight Python command-line tool that analyzes public web pages and reports practical on-page SEO issues. It is designed for developers, independent website owners, digital marketers, and small businesses who want an accessible first-pass SEO audit without paying for expensive SEO platforms.

> **Project status:** Early development (v0.1.0). The current version audits one URL at a time. It is not a full-site crawler, a Google ranking predictor, or a replacement for a professional technical SEO review.

## Features

agentT currently checks:

- HTTP response status and final URL after redirects
- HTML page title and character count
- Meta description and character count
- Canonical URL detection
- H1 presence and count
- Heading structure (H1–H6)
- Images missing an `alt` attribute
- Internal and external link counts
- Links with empty or missing `href`
- Basic robots meta directives

The tool reports observations and simple SEO recommendations. Suggested title and description lengths are guidelines, not Google ranking rules.

## Requirements

- Python 3.10 or newer
- Internet connection to audit public URLs
- No third-party Python dependencies

## Installation

Clone the repository:

```bash
git clone https://github.com/talha4900-alt/agentT.git
```

Navigate into the project directory:

```bash
cd agentT
```

## Usage

Run an SEO audit:

```bash
python -m agentt_seo https://example.com
```

Generate a JSON report:

```bash
python -m agentt_seo https://example.com --json
```

Set a custom request timeout:

```bash
python -m agentt_seo https://example.com --timeout 20
```

On Windows, use `py` if `python` is unavailable:

```powershell
py -m agentt_seo https://example.com
```

The command exits with status code `1` if the page cannot be fetched and `0` when an audit report is produced.

## Development and Testing

Run the test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests are designed to run without requiring a live website.

## Project Structure

```text
agentT/
│
├── agentt_seo/
│   ├── __init__.py
│   ├── __main__.py
│   ├── auditor.py
│   └── parser.py
│
├── tests/
│   ├── test_auditor.py
│   └── test_parser.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── roadmap.md
└── scope-and-limitations.md
```

## Responsible Use

Only audit websites you are authorized to access.

The tool makes a single-page request, follows normal HTTP redirects, and does not attempt to bypass authentication, robots restrictions, rate limits, or other access controls.

Please be considerate when auditing websites you do not own.

For more information:

- [Scope and Limitations](scope-and-limitations.md)
- [Project Roadmap](roadmap.md)

## Contributing

Contributions are welcome!

You can help improve agentT through:

- Bug reports
- Feature suggestions
- Code improvements
- Additional unit tests
- Documentation improvements

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting contributions.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Built by [Talha Ismail](https://github.com/talha4900-alt).

This project is informed by hands-on experience with small-business websites and e-commerce platforms, including WordPress and WooCommerce.

**agentT SEO Auditor is an independent open-source project and is not affiliated with Google or any search engine.**

---

**If you find this project useful, please consider giving it a ⭐ on GitHub!**
