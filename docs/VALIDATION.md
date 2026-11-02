# Module verification — version 2.4.1

Date: November 1, 2026

## Result

All 31 module entrypoints passed controlled functional tests. Live checks returned results for 28 modules. Three metadata modules received HTTP 404 because example.com does not provide those files. CT and OTX initially timed out and succeeded on one manual recheck. No automatic retries were added.

The live smoke tests used example.com, 8.8.8.8, and a synthetic unsigned JWT. They verify execution, transport and response parsing; empty results do not prove complete detection or safety. Authenticated live tests used private local keys, which are not part of the release. Controlled tests use non-secret dummy keys.

## Live checks

| No. | Module | Result | Details |
|---|---|---|---|
| 1 | DNS Over HTTPS | passed | Response received and parsed |
| 2 | DNS Records | passed | Response received and parsed |
| 3 | IP Info | passed | Response received and parsed |
| 4 | Server IP Information | passed | Response received and parsed |
| 5 | TXT Records | passed | Response received and parsed |
| 6 | ASN Lookup | passed | Response received and parsed |
| 7 | DNS CAA Records | passed | Response received and parsed |
| 8 | Archive History | passed | Response received and parsed |
| 9 | Cookies Analyzer | passed | Response received and parsed |
| 10 | Robots.txt Analyzer | not analyzed | HTTP 404 — standard file absent on example.com; controlled positive parsing passed |
| 11 | Sitemap Parsing | not analyzed | HTTP 404 — standard file absent on example.com; controlled positive parsing passed |
| 12 | Social Media Presence Scan | passed | Response received and parsed |
| 13 | Technology Stack Detection | passed | Response received and parsed |
| 14 | Third-Party Integrations | passed | Response received and parsed |
| 15 | Framing Header Check | passed | Response received and parsed |
| 16 | Form Grabber | passed | Response received and parsed |
| 17 | HTML Comments Extractor | passed | Response received and parsed |
| 18 | CAPTCHA Presence Checker | passed | Response received and parsed |
| 19 | Form Autocomplete Inspection | passed | Response received and parsed |
| 20 | Embedded Object Hunter | passed | Response received and parsed |
| 21 | Pixel Tracker Finder | passed | Response received and parsed |
| 22 | Censys Host Records | passed | Response received and parsed |
| 23 | HTTP Headers | passed | Response received and parsed |
| 24 | HTTP Security Features | passed | Response received and parsed |
| 25 | Security.txt Check | not analyzed | HTTP 404 — standard file absent on example.com; controlled positive parsing passed |
| 26 | Shodan Host Records | passed | Response received and parsed |
| 27 | VirusTotal Record Lookup | passed | Response received and parsed |
| 28 | CT Log Query | passed | Response received and parsed; initial attempt timed out |
| 29 | JWT Offline Decoder | passed | Response received and parsed |
| 30 | SPF / DMARC Records | passed | Response received and parsed |
| 31 | AlienVault OTX Threat Intelligence | passed | Response received and parsed; initial attempt timed out |

## Explanation of the reported eBay behavior

One GET to https://ebay.com returned HTTP 301 pointing to https://www.ebay.com/. Redirects remain disabled. One separate GET to the canonical destination returned HTTP 403. The tool cannot analyze the final page when access is denied; it does not bypass the denial. These results must not be presented as zero social profiles.

## Fixes included

- Redirects now return `outcome: not_analyzed`, the HTTP status, the destination, and input guidance where the destination is a valid origin. No destination is fetched automatically.
- Non-success HTTP responses no longer flow into page parsers or return misleading empty findings.
- The menu says “Not analyzed” instead of “Finished” for these outcomes.
- Timeout, connection and TLS failures have readable messages without exposing API keys or request URLs.
- Namespaced XML sitemaps are parsed correctly. Malformed XML and DTD/entity declarations are rejected.
- Malformed links are ignored instead of crashing social-link/integration extraction.
- Scheme/port mismatches are rejected rather than silently rewritten.
- Social-link output explicitly describes its scope: static links in the one fetched HTML page. No JavaScript, crawling, or search-engine checks.

## Automated verification

215 mock-based checks passed, including a controlled dispatch for every module, positive fixtures with known findings, and blocked/error status handling for every website module. Existing allowlist, credential isolation, request-budget, TLS, redirect, and input-validation checks also passed.

This does not guarantee success on every site or provider account. Sites can deny automated requests, hide links behind JavaScript, omit metadata, or require authentication. Provider permissions, quotas and availability vary. No intrusive scans or bypasses were used during this verification.
