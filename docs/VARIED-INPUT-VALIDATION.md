# ThreatHawk: varied-input verification

Date: November 1, 2026. Local version: 2.6.1. GitHub was not modified.

## Results

All 22 modules produced a completed result for at least one input. 81 module/input cases were checked: 53 completed, 18 returned redirects, 9 received website access denials, and 1 metadata file was not found. No uncaught code failures, provider authentication failures, or timeouts occurred in this run. Two JWT cases were offline; other cases used live DNS/provider data or freshly fetched website responses.

The website parsers shared the same in-memory response for each identical URL, avoiding repeated requests to a site. There were 12 distinct website GETs. Thus 81 cases does not mean 81 independent network requests. The test cache was in memory only; provider credentials and page bodies are not included in this report.

## Reported module 09

| Input | Actual result |
|---|---|
| `https://google.com` | HTTP 301 → `https://www.google.com/`; destination not followed automatically |
| `https://www.google.com` | HTTP 200; server hint `gws` |
| `https://ebay.com` | HTTP 301 → `https://www.ebay.com/`; destination not followed automatically |
| `https://www.ebay.com` | HTTP 403; website denied access; no bypass attempted |
| `https://www.python.org` | HTTP 200; server hint `nginx`; 6 referenced integration hosts |
| `https://example.com` | HTTP 200; server hint `cloudflare`; no referenced integration hosts |

These observations are response-specific, not complete technology inventories. JavaScript is not executed, linked assets are not fetched, and headers may be omitted or misleading.

## Module-by-module cases

| No. | Module | Input | Outcome |
|---|---|---|---|
| 01 | DNS Over HTTPS | `example.com` | passed |
| 01 | DNS Over HTTPS | `python.org` | passed |
| 02 | DNS & Email Records | `example.com` | passed |
| 02 | DNS & Email Records | `python.org` | passed |
| 03 | IP & ASN Information | `8.8.8.8` | passed |
| 03 | IP & ASN Information | `1.1.1.1` | passed |
| 04 | Archive History | `example.com` | passed |
| 04 | Archive History | `python.org` | passed |
| 05 | Cookies Analyzer | `https://example.com` | passed · HTTP 200 |
| 05 | Cookies Analyzer | `https://www.python.org` | passed · HTTP 200 |
| 05 | Cookies Analyzer | `https://google.com` | not analyzed · HTTP 301 |
| 05 | Cookies Analyzer | `https://www.google.com` | passed · HTTP 200 |
| 05 | Cookies Analyzer | `https://ebay.com` | not analyzed · HTTP 301 |
| 05 | Cookies Analyzer | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 06 | Robots.txt Analyzer | `https://www.google.com` | passed · HTTP 200 |
| 06 | Robots.txt Analyzer | `https://www.python.org` | passed · HTTP 200 |
| 07 | Sitemap Parsing | `https://www.djangoproject.com` | passed · HTTP 200 |
| 07 | Sitemap Parsing | `https://www.google.com` | passed · HTTP 200 |
| 08 | Social Links Inspection | `https://example.com` | passed · HTTP 200 |
| 08 | Social Links Inspection | `https://www.python.org` | passed · HTTP 200 |
| 08 | Social Links Inspection | `https://google.com` | not analyzed · HTTP 301 |
| 08 | Social Links Inspection | `https://www.google.com` | passed · HTTP 200 |
| 08 | Social Links Inspection | `https://ebay.com` | not analyzed · HTTP 301 |
| 08 | Social Links Inspection | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 09 | Technology & Integrations | `https://example.com` | passed · HTTP 200 |
| 09 | Technology & Integrations | `https://www.python.org` | passed · HTTP 200 |
| 09 | Technology & Integrations | `https://google.com` | not analyzed · HTTP 301 |
| 09 | Technology & Integrations | `https://www.google.com` | passed · HTTP 200 |
| 09 | Technology & Integrations | `https://ebay.com` | not analyzed · HTTP 301 |
| 09 | Technology & Integrations | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 10 | Form & Autocomplete Inspection | `https://example.com` | passed · HTTP 200 |
| 10 | Form & Autocomplete Inspection | `https://www.python.org` | passed · HTTP 200 |
| 10 | Form & Autocomplete Inspection | `https://google.com` | not analyzed · HTTP 301 |
| 10 | Form & Autocomplete Inspection | `https://www.google.com` | passed · HTTP 200 |
| 10 | Form & Autocomplete Inspection | `https://ebay.com` | not analyzed · HTTP 301 |
| 10 | Form & Autocomplete Inspection | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 11 | HTML Comments Extractor | `https://example.com` | passed · HTTP 200 |
| 11 | HTML Comments Extractor | `https://www.python.org` | passed · HTTP 200 |
| 11 | HTML Comments Extractor | `https://google.com` | not analyzed · HTTP 301 |
| 11 | HTML Comments Extractor | `https://www.google.com` | passed · HTTP 200 |
| 11 | HTML Comments Extractor | `https://ebay.com` | not analyzed · HTTP 301 |
| 11 | HTML Comments Extractor | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 12 | CAPTCHA Presence Checker | `https://example.com` | passed · HTTP 200 |
| 12 | CAPTCHA Presence Checker | `https://www.python.org` | passed · HTTP 200 |
| 12 | CAPTCHA Presence Checker | `https://google.com` | not analyzed · HTTP 301 |
| 12 | CAPTCHA Presence Checker | `https://www.google.com` | passed · HTTP 200 |
| 12 | CAPTCHA Presence Checker | `https://ebay.com` | not analyzed · HTTP 301 |
| 12 | CAPTCHA Presence Checker | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 13 | Embedded Object Hunter | `https://example.com` | passed · HTTP 200 |
| 13 | Embedded Object Hunter | `https://www.python.org` | passed · HTTP 200 |
| 13 | Embedded Object Hunter | `https://google.com` | not analyzed · HTTP 301 |
| 13 | Embedded Object Hunter | `https://www.google.com` | passed · HTTP 200 |
| 13 | Embedded Object Hunter | `https://ebay.com` | not analyzed · HTTP 301 |
| 13 | Embedded Object Hunter | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 14 | Pixel Tracker Finder | `https://example.com` | passed · HTTP 200 |
| 14 | Pixel Tracker Finder | `https://www.python.org` | passed · HTTP 200 |
| 14 | Pixel Tracker Finder | `https://google.com` | not analyzed · HTTP 301 |
| 14 | Pixel Tracker Finder | `https://www.google.com` | passed · HTTP 200 |
| 14 | Pixel Tracker Finder | `https://ebay.com` | not analyzed · HTTP 301 |
| 14 | Pixel Tracker Finder | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 15 | Censys Host Records | `8.8.8.8` | passed |
| 15 | Censys Host Records | `1.1.1.1` | passed |
| 16 | HTTP Security & Headers | `https://example.com` | passed · HTTP 200 |
| 16 | HTTP Security & Headers | `https://www.python.org` | passed · HTTP 200 |
| 16 | HTTP Security & Headers | `https://google.com` | not analyzed · HTTP 301 |
| 16 | HTTP Security & Headers | `https://www.google.com` | passed · HTTP 200 |
| 16 | HTTP Security & Headers | `https://ebay.com` | not analyzed · HTTP 301 |
| 16 | HTTP Security & Headers | `https://www.ebay.com` | not analyzed · HTTP 403 |
| 17 | Security.txt Check | `https://www.google.com` | passed · HTTP 200 |
| 17 | Security.txt Check | `https://www.python.org` | not analyzed · HTTP 404 |
| 18 | Shodan Host Records | `8.8.8.8` | passed |
| 18 | Shodan Host Records | `1.1.1.1` | passed |
| 19 | VirusTotal Record Lookup | `8.8.8.8` | passed |
| 19 | VirusTotal Record Lookup | `example.com` | passed |
| 20 | CT Log Query | `example.com` | passed |
| 20 | CT Log Query | `python.org` | passed |
| 21 | JWT Offline Decoder | `Synthetic offline JWT` | passed |
| 21 | JWT Offline Decoder | `Synthetic offline JWT` | passed |
| 22 | AlienVault OTX Threat Intelligence | `8.8.8.8` | passed |
| 22 | AlienVault OTX Threat Intelligence | `example.com` | passed |
| 22 | AlienVault OTX Threat Intelligence | `d41d8cd98f00b204e9800998ecf8427e` | passed |

## Local fixes

- Add an explicit `r` action after a same-site HTTPS origin/`www` redirect. Only typing `r` makes the separate request. No automatic redirect following was added.
- The shortcut does not offer cross-site redirects, credentials, queries, fragments, custom ports, arbitrary paths or HTTPS downgrades. It is cleared when changing modules or making another run. A website denial is not retried or bypassed automatically.
- Improve messages for moved websites and HTTP 403.
- Parse XML sitemaps with the XML parser only, eliminating the misleading HTML-parser warning observed in the live checks. DTD/entity restrictions remain.
- Preserve the previous local removal of the “TERMINAL ONLY” startup label.

219 automated checks passed. An end-to-end live Terminal flow from `google.com` → explicit `r` → `www.google.com` returned the `gws` server hint successfully. No GitHub changes were made.

## Useful examples

- Technology, forms, headers, links and other homepage checks: `https://www.python.org` or `https://www.google.com`.
- Sitemap: `https://www.djangoproject.com` or `https://www.google.com`.
- Robots: `https://www.python.org` or `https://www.google.com`.
- Security.txt: `https://www.google.com`. The Python site returned 404 for that specific metadata file.
- DNS/DoH/CT/archive: `example.com` or `python.org`.
- IP/Censys/Shodan: `8.8.8.8` or `1.1.1.1` (tested plan permissions may differ for other IPs).
- VirusTotal: `8.8.8.8` or `example.com`.
- OTX: `8.8.8.8`, `example.com`, or hash `d41d8cd98f00b204e9800998ecf8427e`.

Website samples are ordinary single-page GETs or standard metadata checks. This verification does not authorize scans against arbitrary systems or guarantee provider/site availability, completeness or safety. Redirects and denials are expected network outcomes rather than proof of a broken module.
