# Scope and limitations

## What version 0.1.0 does

agentT SEO Auditor requests one URL, reads its HTML response, and extracts common on-page elements: title, meta description, canonical URL, robots meta, headings, image alt attributes, and link counts. It produces a terminal report or JSON.

The first version uses Python's standard library and does not require an API key or third-party service.

## What it does not do

- It does not crawl an entire website or discover URLs from a sitemap.
- It does not execute JavaScript or render a browser DOM.
- It does not check whether every link returns a successful response.
- It does not inspect structured data, Core Web Vitals, page speed, backlinks, rankings, or Search Console data.
- It does not determine whether a page is indexed or predict rankings.

## Interpreting results

Suggested title and description character ranges are broad editorial heuristics, not ranking rules. Search engines may display different snippets and do not guarantee a particular title or description length.

An image with an empty alt attribute may be intentionally decorative. This version reports missing alt attributes but does not decide whether each image needs descriptive alternative text.

The tool reports a canonical URL when present but does not verify whether it is the correct preferred URL.

## Responsible use

The tool makes one page request per run, follows HTTP redirects, and reads at most 2 MB of response content. Only audit sites you own or have permission to test. Do not use repeated requests to overload websites.
