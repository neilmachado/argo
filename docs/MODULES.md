# Module reference — version 2.5

Modules are numbered 01–22 after merging overlapping checks. IDs from earlier versions have changed. Select a module number to see its exact API/source, endpoint, required input, example and credential status.

| No. | Module | Input | API / source |
|---|---|---|---|
| 01 | DNS Over HTTPS | Domain | API: Google DNS-over-HTTPS |
| 02 | DNS & Email Records | Domain | Source: System DNS resolver |
| 03 | IP & ASN Information | IPv4 / IPv6 | API: ipwho.is IP information |
| 04 | Archive History | Domain | API: Internet Archive Wayback CDX |
| 05 | Cookies Analyzer | Domain / HTTP(S) origin | Source: Website response · No external API |
| 06 | Robots.txt Analyzer | Domain / HTTP(S) origin | Source: Website response · No external API |
| 07 | Sitemap Parsing | Domain / HTTP(S) origin | Source: Website response · No external API |
| 08 | Social Links Inspection | Domain / HTTP(S) origin | Source: Website response · No external API |
| 09 | Technology & Integrations | Domain / HTTP(S) origin | Source: Website response · No external API |
| 10 | Form & Autocomplete Inspection | Domain / HTTP(S) origin | Source: Website response · No external API |
| 11 | HTML Comments Extractor | Domain / HTTP(S) origin | Source: Website response · No external API |
| 12 | CAPTCHA Presence Checker | Domain / HTTP(S) origin | Source: Website response · No external API |
| 13 | Embedded Object Hunter | Domain / HTTP(S) origin | Source: Website response · No external API |
| 14 | Pixel Tracker Finder | Domain / HTTP(S) origin | Source: Website response · No external API |
| 15 | Censys Host Records | IPv4 / IPv6 | API: Censys Platform API · Host Records |
| 16 | HTTP Security & Headers | Domain / HTTP(S) origin | Source: Website response · No external API |
| 17 | Security.txt Check | Domain / HTTP(S) origin | Source: Website response · No external API |
| 18 | Shodan Host Records | IPv4 / IPv6 | API: Shodan Host API |
| 19 | VirusTotal Record Lookup | Domain / IP | API: VirusTotal API v3 |
| 20 | CT Log Query | Domain | API: crt.sh Certificate Transparency |
| 21 | JWT Offline Decoder | JWT token | Source: Offline JWT decoder |
| 22 | AlienVault OTX Threat Intelligence | IP / domain / MD5 / SHA-1 / SHA-256 | API: AlienVault OTX Indicator API |

## Combined checks

- IP Info, Server IP Information and ASN Lookup → **IP & ASN Information**.
- DNS Records, TXT Records, CAA and SPF/DMARC → **DNS & Email Records**.
- HTTP Headers, HTTP Security Features and Framing Header Check → **HTTP Security & Headers**.
- Form Grabber and Autocomplete Inspection → **Form & Autocomplete Inspection**.
- Technology Stack and Third-Party Integrations → **Technology & Integrations**.

Threat-intelligence providers remain separate because their coverage differs. DNS-over-HTTPS remains separate because it uses a different transport and provider.
