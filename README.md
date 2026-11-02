![Arugus by Neil](assets/banner.svg)

# Arugus by Neil

A terminal toolkit for DNS, public-record lookups, offline JWT inspection, and bounded website checks. Built on Argus, with intrusive scanning modules excluded.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2EC4B6)
![Modules](https://img.shields.io/badge/Modules-31-2EC4B6)

[Quick start](#install) · [Module reference](docs/MODULES.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

⚠️ WARNING: LEGAL DISCLAIMER

This tool is intended for **educational and ethical use only**. The author is not liable for any illegal use or misuse of this tool. Users are solely responsible for their actions and must ensure they have explicit permission to scan the target systems.

## Capabilities

This edition contains **31 modules**. It restores 25 useful checks with constrained implementations, while excluding 117 original module files. Modules are numbered consecutively from 01 to 31. Choose option 1 to view the list.

- Records: Censys, Shodan, VirusTotal domain/IP reports, AlienVault OTX indicator intelligence, certificate transparency, Wayback archive listings, IP/ASN/server IP information.
- DNS: standard records, TXT, CAA, SPF/DMARC inspection, and DNS-over-HTTPS. No AXFR, dictionary enumeration, DKIM selector guessing, or recursive SPF expansion.
- Website inspection: headers, cookie attributes, security/framing headers, security.txt, robots.txt, sitemap locations, comments, forms/autocomplete, CAPTCHA indicators, social links, embedded objects, possible tracking pixels, generator/server technology hints, referenced integration hosts.
- Offline: JWT header/payload decoding. This does NOT validate signatures or establish that a token is trustworthy.

Website checks make **one GET per module invocation**, to the supplied origin homepage or one standard metadata path. They do not crawl, follow redirects, execute scripts, fetch linked assets, submit forms, guess paths, or mutate resources. These are low-impact active requests, not passive lookups. Use them only with permission. A misleading or state-changing target GET endpoint can still have side effects; no tool can guarantee otherwise. The menu runs only the selected module.

Censys and Shodan accept an IP only. IP/ASN/server information also accepts an IP only. VirusTotal accepts a domain/IP, not a URL. DNS and CT require a bare domain. JWT takes a token. Website checks accept a bare domain or HTTP(S) origin; arbitrary paths, queries, credentials and custom ports are rejected. No automatic HTTP fallback or redirect following is performed; redirects are reported for the user to inspect.

Historical lookups share lookup terms with providers. DNS queries use the configured resolver and may reach authoritative nameservers. CAA and TXT each make one resolver call, SPF/DMARC makes two, and standard DNS queries seven fixed record types; DNS transport may retry under resolver rules. DoH uses Google's fixed JSON resolver endpoint. Archive listings are limited to 50 entries and never fetched. HTTP bodies are limited to 2 MB, TLS certificates are verified, ambient proxies disabled, and no automatic HTTP retries are configured.

No port scans, fuzzing, WAF bypass tests, password/community guessing, AXFR, state-changing HTTP method tests, cloud bucket enumeration, secret-file discovery, PageSpeed/SSL Labs tests, or scan submissions are shipped. No automatic result files, reports, disk caches or run logs are written. Terminal scrollback and shell capture may retain output.

These are intentionally smaller implementations than the original modules: a homepage-only check may miss site-wide behavior. Technology/CAPTCHA/pixel/header observations are hints, not proof of vulnerabilities or complete detection. Cookies are parsed from response headers without printing values. Redirection and transport failures are shown without attempting broader probes. Third-party integration output lists referenced hosts; it does not prove a business relationship or that every host is third party.

## Install

Use Python 3.10 or newer. First download the repository, or clone it:

```sh
git clone https://github.com/neilmachado/Argus-By-neil.git
cd Argus-By-neil
python3 -m venv .venv
source .venv/bin/activate
pip install .
cp .env.example .env
# Edit .env locally with your own keys; never commit it.
set -a
source .env
set +a
python -m argus
```

The home screen has exactly four options:

```text
1. View modules
2. Select module
3. Run module
4. Exit
```

1. Choose **1** or **2** to open the module list. Enter a module number to select it.
2. The selected module shows its input type, example and API-key requirement. Type the required input directly to run it, or press **Enter** for a guided input prompt.
3. Enter the requested input. Results appear directly in Terminal.
4. After results, enter a new input directly or press **Enter** to run the selected module again, **b** to return home, or **q** to exit.

The home menu appears again only when you explicitly return home. Each section shows just its relevant prompt. From home, option **3** runs the selected module directly, and option **4** exits. If no module is selected, option 3 guides you to select one.

Example: choose **2**, enter **2** for DNS Records, press **Enter**, then enter `example.com`. No API key is required. A domain-only module rejects IPs, email addresses and URLs before making a request. IP modules accept IPv4/IPv6 addresses. Website modules accept a domain or HTTP(S) origin. The offline JWT decoder accepts a JWT. Email addresses are not supported. AlienVault OTX (module 31) additionally accepts MD5, SHA-1 and SHA-256 hashes.

Blank target input cancels the run. In the module list, **b** or an empty selection returns home and **q** exits. Invalid module numbers keep you in the selection section. Each run asks for fresh input; there is no `use`, `set target`, `run`, or `help` syntax to memorize.

The DNS lookup needs no key. Censys uses CENSYS_PAT, Shodan uses SHODAN_API_KEY, and VirusTotal uses VIRUSTOTAL_API_KEY. Provider plans and rate limits still apply. A configured key is not a guarantee of record access: Shodan may return HTTP 403 for a host requiring membership or a higher plan. HTTP 404 indicates no record, 401 indicates an authentication failure, and 429 indicates rate limiting. The `.env` file is loaded only when you source it as shown above; the program does not auto-load it. Google keys are not used in this edition.

## AlienVault OTX (module 31)

Looks up existing general indicator intelligence using the [official OTX indicator API](https://github.com/AlienVault-OTX/OTX-Python-SDK). Accepts IPv4, IPv6, bare domains, and hexadecimal MD5 (32), SHA-1 (40), or SHA-256 (64-character) hashes. It does not accept emails, URLs, CIDRs, local file paths or file uploads. Indicator type is detected automatically.

Get your own API key from your [OTX account/API page](https://otx.alienvault.com/api), set `OTX_API_KEY` in your local environment or private `.env`, source it, and restart the tool. Do not commit or paste real API keys into issues or chat.

The module makes one GET to `https://otx.alienvault.com/api/v1/indicators/{type}/{indicator}/general`, sends only the OTX key in the `X-OTX-API-KEY` header, and follows no returned links. Hash types use the API's `file` type. No target system is contacted or scanned, no files or URLs are submitted, and no pulse is created. The lookup indicator is disclosed to OTX. A pulse association is not a conclusive maliciousness verdict, and no match does not establish safety. Authenticated OTX lookup for 8.8.8.8 was verified locally. API keys remain private and are not included in this repository.

## Redirects, denied access and missing metadata

A 301/302 response is a redirect, not a successful content analysis. The tool displays the destination without following it. Enter the canonical origin separately only if you are permitted to check it. HTTP 403 means access was denied, and HTTP 404 means the requested page/file was not found. These responses show `outcome: not_analyzed`; an empty findings list is not fabricated. A 200-page with no static social links does not prove the site has no social accounts or JavaScript-loaded links.

See [the module verification report](docs/VALIDATION.md) for the all-module checks and sample outcomes.

## Verification

```sh
pip install pytest
python -m pytest tests -q
```

Tests use mocks, not live scans. They verify physical module removal, catalog restrictions, forbidden runner paths, HTTP destinations, GET-only lookups, TLS, redirect refusal, response size limits, fixed DNS record types, bounded website requests, no form submissions offline JWT decoding, consecutive module IDs, input validation and the four-option menu flow. Dependencies have not received a full security audit.

## Project structure

```text
argus/               CLI, reviewed dispatch and bounded lookup implementations
  modules/           31 module entrypoints
  passive.py         Fixed-provider HTTP lookup client and module allowlist
  nonintrusive.py    Bounded website/DNS checks and offline decoder
tests/               Mock-based safety and behavior tests
docs/MODULES.md      Inputs and behavior for each module
.env.example         Credential placeholders only
```

See [CHANGELOG.md](CHANGELOG.md) for release notes and [RESTORATION.md](RESTORATION.md) for implementation limits. The [excluded module list](removed-modules.json) documents what is not shipped.

## Attribution

Based on [divinelabio/Argus](https://github.com/divinelabio/Argus), originally credited to Jasonxtn / Jason13. Neil customized the branding, terminal-only output, Censys PAT support and restricted record-lookup edition. Original MIT copyright and license notices are retained in LICENSE.
