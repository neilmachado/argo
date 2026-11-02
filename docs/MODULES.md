# Module reference

From home, choose **1** or **2**, then enter a module number. Press **Enter** to run and supply the requested input. After results, **Enter** runs again, **b** returns home, and **q** exits. Home options **3** and **4** run the current selection and exit respectively. Numbers 01–31 replace the original sparse IDs. Leading zeros are optional.

| No. | Module | Required input | Example |
|---|---|---|---|
| 01 | DNS Over HTTPS | Domain name | `example.com` |
| 02 | DNS Records | Domain name | `example.com` |
| 03 | IP Info | IPv4 / IPv6 | `8.8.8.8` |
| 04 | Server IP Information | IPv4 / IPv6 | `8.8.8.8` |
| 05 | TXT Records | Domain name | `example.com` |
| 06 | ASN Lookup | IPv4 / IPv6 | `8.8.8.8` |
| 07 | DNS CAA Records | Domain name | `example.com` |
| 08 | Archive History | Domain name | `example.com` |
| 09 | Cookies Analyzer | Domain / HTTP(S) origin | `https://example.com` |
| 10 | Robots.txt Analyzer | Domain / HTTP(S) origin | `https://example.com` |
| 11 | Sitemap Parsing | Domain / HTTP(S) origin | `https://example.com` |
| 12 | Social Media Presence Scan | Domain / HTTP(S) origin | `https://example.com` |
| 13 | Technology Stack Detection | Domain / HTTP(S) origin | `https://example.com` |
| 14 | Third-Party Integrations | Domain / HTTP(S) origin | `https://example.com` |
| 15 | Framing Header Check | Domain / HTTP(S) origin | `https://example.com` |
| 16 | Form Grabber | Domain / HTTP(S) origin | `https://example.com` |
| 17 | HTML Comments Extractor | Domain / HTTP(S) origin | `https://example.com` |
| 18 | CAPTCHA Presence Checker | Domain / HTTP(S) origin | `https://example.com` |
| 19 | Form Autocomplete Inspection | Domain / HTTP(S) origin | `https://example.com` |
| 20 | Embedded Object Hunter | Domain / HTTP(S) origin | `https://example.com` |
| 21 | Pixel Tracker Finder | Domain / HTTP(S) origin | `https://example.com` |
| 22 | Censys Host Records | IPv4 / IPv6 | `8.8.8.8` |
| 23 | HTTP Headers | Domain / HTTP(S) origin | `https://example.com` |
| 24 | HTTP Security Features | Domain / HTTP(S) origin | `https://example.com` |
| 25 | Security.txt Check | Domain / HTTP(S) origin | `https://example.com` |
| 26 | Shodan Host Records | IPv4 / IPv6 | `8.8.8.8` |
| 27 | VirusTotal Record Lookup | Domain / IP | `example.com or 8.8.8.8` |
| 28 | CT Log Query | Domain name | `example.com` |
| 29 | JWT Offline Decoder | JWT token | `eyJhbGciOiJub25lIn0.eyJzdWIiOiJleGFtcGxlIn0.` |
| 30 | SPF / DMARC Records | Domain name | `example.com` |

| 31 | AlienVault OTX Threat Intelligence | IP / domain / MD5 / SHA-1 / SHA-256 | `8.8.8.8` or `example.com` |

Website checks inspect one page or standard metadata path; they do not crawl or submit forms. Domain means a bare hostname, without a scheme/path or email address. Email addresses are unsupported. Hash input is accepted only by AlienVault OTX (31). JWT decoding is offline and does not verify signatures.
