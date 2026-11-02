# Module reference

Use `modules` inside the CLI to see these IDs. Set an input with `set target <value>`, select with `use <id>`, then run `run`.

| ID | Module | Input | Behavior |
|---|---|---|---|
| 2 | DNS Over HTTPS | Domain | Bounded DNS record lookup; no AXFR, selector guessing or recursive expansion. |
| 3 | DNS Records | Domain | Ordinary DNS resolver queries only: A, AAAA, MX, NS, TXT, CNAME, SOA. No AXFR or brute force. |
| 8 | IP Info | IP | Public IP information from ipwho.is only; no target connection. |
| 10 | Server IP Information | IP | Public IP information from ipwho.is only; no target connection. |
| 17 | TXT Records | Domain | Bounded DNS record lookup; no AXFR, selector guessing or recursive expansion. |
| 20 | ASN Lookup | IP | Public IP information from ipwho.is only; no target connection. |
| 45 | Archive History | Domain | Up to 50 existing Wayback CDX records; archived URLs are not fetched. |
| 49 | Cookies Analyzer | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 52 | Robots.txt Analyzer | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 58 | Sitemap Parsing | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 59 | Social Media Presence Scan | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 60 | Technology Stack Detection | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 61 | Third-Party Integrations | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 66 | Framing Header Check | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 67 | Form Grabber | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 69 | HTML Comments Extractor | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 70 | CAPTCHA Presence Checker | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 75 | Form Autocomplete Inspection | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 76 | Embedded Object Hunter | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 78 | Pixel Tracker Finder | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 93 | Censys Host Records | IP | Retrieve an existing host record from Censys; no target connection. |
| 99 | HTTP Headers | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 100 | HTTP Security Features | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 104 | Security.txt Check | Domain | One page/standard metadata GET only; no crawling, form submission, asset loading or redirects. |
| 105 | Shodan Host Records | IP | Retrieve an existing Shodan host record; no scan submission. |
| 110 | VirusTotal Record Lookup | Domain/IP | Read existing domain/IP reports only; no URL scan submissions. |
| 111 | CT Log Query | Domain | Query existing certificate transparency records at crt.sh. |
| 114 | JWT Offline Decoder | JWT | Offline JWT header/payload decoder; signature is NOT verified. |
| 118 | SPF / DMARC Records | Domain | Bounded DNS record lookup; no AXFR, selector guessing or recursive expansion. |
| 139 | DNS CAA Records | Domain | Ordinary CAA lookup for the supplied domain only; no subdomain guessing. |

Website observations are homepage-only unless the module uses a standard metadata path. They are not site-wide vulnerability assessments. See the README for request limits and provider disclosure.
