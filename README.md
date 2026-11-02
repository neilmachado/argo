# ThreatHawk

A terminal toolkit for DNS, public-record lookups, offline JWT inspection, and bounded website checks. Related checks are combined into **22 modules**, with the API or data source displayed before every run.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2EC4B6)
![Modules](https://img.shields.io/badge/Modules-22-2EC4B6)

[Install](#install) · [Module reference](docs/MODULES.md) · [Verification](docs/VALIDATION.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

## ⚠️ WARNING: LEGAL DISCLAIMER

This tool is intended for **educational and ethical use only**. The author is not liable for any illegal use or misuse of this tool. Users are solely responsible for their actions and must ensure they have explicit permission to scan the target systems.

## Capabilities

- **DNS & Email Records:** A, AAAA, MX, NS, TXT, CNAME, SOA, CAA, SPF and DMARC. Nine fixed resolver queries; the TXT response is reused for SPF. No AXFR, guessing or recursive SPF expansion.
- **IP & ASN Information:** IP location, organization, server IP details and ASN from one ipwho.is request.
- **HTTP Security & Headers:** raw response headers, security headers and framing policy from one homepage GET.
- **Form & Autocomplete Inspection:** form methods, actions, field types and autocomplete attributes from one homepage GET. No field values or submissions.
- **Technology & Integrations:** server/generator hints and referenced integration hosts from one homepage GET. No linked assets are fetched.
- Separate, bounded checks for cookies, robots.txt, sitemaps, static social links, comments, CAPTCHA indicators, embedded objects, tracking-pixel hints and security.txt.
- Distinct record sources: Censys, Shodan, VirusTotal, AlienVault OTX, certificate transparency, Wayback and Google DNS-over-HTTPS. Their different data coverage is retained.
- Offline JWT decoding. Signatures and claims are **not verified**.

See the [module reference](docs/MODULES.md) for IDs **01–22**, input examples and sources. Older module numbers have changed.

## APIs and data sources

| Module/source | API used | Credential |
|---|---|---|
| Censys Host Records | Censys Platform API, host record endpoint | `CENSYS_PAT` |
| Shodan Host Records | Shodan Host API | `SHODAN_API_KEY` |
| VirusTotal Record Lookup | VirusTotal API v3, existing IP/domain reports | `VIRUSTOTAL_API_KEY` |
| AlienVault OTX Threat Intelligence | OTX Indicator API, existing general records | `OTX_API_KEY` |
| IP & ASN Information | ipwho.is | None |
| Archive History | Internet Archive Wayback CDX | None |
| CT Log Query | crt.sh certificate transparency | None |
| DNS Over HTTPS | Google DNS JSON resolver | None |
| DNS & Email Records | System DNS resolver; no HTTP API | None |
| Website checks | Supplied website response; no external intelligence API | None |
| JWT Offline Decoder | Local processing; no API/network request | None |

The exact source and endpoint template appear at selection and immediately before execution. Real credential values are never shown there. A configured key does not guarantee access to every record: account plans, permissions and rate limits still apply. Google API keys are not used.

## Install

Use Python 3.10 or newer:

```sh
git clone https://github.com/neilmachado/ThreatHawk.git
cd ThreatHawk
python3 -m venv .venv
source .venv/bin/activate
pip install .
cp .env.example .env
# Edit .env privately with your own provider keys; never commit real keys.
set -a
source .env
set +a
python -m threathawk
```

The program does not auto-load `.env`; source it as above. DNS and ordinary website checks work without provider keys. Do not paste real credentials into chat, issues or source files.

## Guided use

The home screen contains four options:

```text
1. View modules
2. Select module
3. Run module
4. Exit
```

Choose **1** or **2**, then enter a module number. Selection shows the input type, an example, the API/source and credential status. Type the input directly to run, or press Enter for input guidance. After results, type another input to run again, **b** for home or **q** to exit. When a same-site HTTPS/`www` redirect is reported, **r** explicitly requests that destination once; it is never fetched automatically. Home option 3 runs the selected module; without a selection it guides you to choose one. The home menu does not repeat inside each section.

Example: choose **2**, enter **2** for DNS & Email Records, then type `example.com`. IP modules require IPv4/IPv6; website modules accept a domain or HTTP(S) origin. Domain-only modules reject IPs, paths and email addresses. AlienVault OTX accepts IPs, domains and hexadecimal MD5/SHA-1/SHA-256 hashes, detected automatically. Email addresses, URLs and file uploads are not supported by OTX in this tool.

## Request boundaries and limitations

Website checks make one GET to the homepage or one standard metadata path. No crawling, form submissions, JavaScript execution, linked-resource fetching, automatic redirect following or automatic retries. TLS verification is enabled, response sizes are limited to 2 MB and timeouts are finite. Website checks are low-impact active requests that require permission; GET is not a universal guarantee against side effects. DNS resolvers may retry under their own rules.

Redirects display `outcome: not_analyzed`, the destination and next-step guidance where applicable. For same-site HTTPS origin/`www` moves only, the contextual `r` shortcut makes one separate request after explicit user input. Enter the canonical origin separately only if authorized. Denied requests, missing files and network errors are not reported as zero findings. HTTP 403 can reflect a provider restriction or website access denial. A page with no static social links does not prove there are no social accounts or JavaScript-loaded links.

Header, CAPTCHA, technology and pixel findings are observations, not proven vulnerabilities or complete assessments. Pulse associations do not conclusively establish maliciousness, and no matches do not establish safety. Lookups disclose indicators to providers. OTX uses existing indicator GETs only, not uploads, scan submissions or pulse creation. Archive URLs and sitemap entries are listed without fetching them.

Intrusive scanning modules remain excluded. No automatic result files, reports, run logs or disk response caches are written. Terminal scrollback, external shell capture and provider logs may retain data. No legal or security certification is implied.

[Varied-input module checks and useful examples](docs/VARIED-INPUT-VALIDATION.md).

## Verification

```sh
pip install pytest
python -m pytest tests -q
```

See [current verification](docs/VALIDATION.md) and the [historical 2.4.1 module audit](docs/VALIDATION-2.4.1.md). Mock-based tests cover every retained module, merged outputs, single-response reuse, displayed sources, input validation, credential isolation and network boundaries. Dependencies have not received a full independent audit.

## Branding

The public distribution uses text-only ThreatHawk branding. It contains no portrait logo or derived portrait artwork. The command is `threathawk` (or `python -m threathawk`); `argus` remains a compatibility command.

## Attribution

Based on [divinelabio/Argus](https://github.com/divinelabio/Argus), originally credited to Jasonxtn / Jason13. Neil customized branding, terminal-only output, Censys PAT support, restricted implementations and the guided interface. The original MIT copyright/permission notice is retained in LICENSE.
