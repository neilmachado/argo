![Arugus by Neil](assets/banner.svg)

# Arugus by Neil

A terminal toolkit for DNS, public-record lookups, offline JWT inspection, and bounded website checks. Built on Argus, with intrusive scanning modules excluded.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2EC4B6)
![Modules](https://img.shields.io/badge/Modules-30-2EC4B6)

[Quick start](#install) · [Module reference](docs/MODULES.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md)

⚠️ WARNING: LEGAL DISCLAIMER

This tool is intended for **educational and ethical use only**. The author is not liable for any illegal use or misuse of this tool. Users are solely responsible for their actions and must ensure they have explicit permission to scan the target systems.

## Capabilities

This edition contains **30 modules**. It restores 25 useful checks with constrained implementations, while excluding 117 original module files. Module IDs remain compatible with the original catalog where available. Use `modules` to list them.

- Records: Censys, Shodan, VirusTotal domain/IP reports, certificate transparency, Wayback archive listings, IP/ASN/server IP information.
- DNS: standard records, TXT, CAA, SPF/DMARC inspection, and DNS-over-HTTPS. No AXFR, dictionary enumeration, DKIM selector guessing, or recursive SPF expansion.
- Website inspection: headers, cookie attributes, security/framing headers, security.txt, robots.txt, sitemap locations, comments, forms/autocomplete, CAPTCHA indicators, social links, embedded objects, possible tracking pixels, generator/server technology hints, referenced integration hosts.
- Offline: JWT header/payload decoding. This does NOT validate signatures or establish that a token is trustworthy.

Website checks make **one GET per module invocation**, to the supplied origin homepage or one standard metadata path. They do not crawl, follow redirects, execute scripts, fetch linked assets, submit forms, guess paths, or mutate resources. These are low-impact active requests, not passive lookups. Use them only with permission. A misleading or state-changing target GET endpoint can still have side effects; no tool can guarantee otherwise. Batch commands may make several independent checks, one after another.

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

Example commands inside the CLI:

```text
modules
use 3
set target example.com
run
exit
```

This example uses module 3 (DNS Records), which requires no API key. To use Censys, run `search censys`, select the number shown with `use <number>`, and set an IP target such as `8.8.8.8`.

The DNS lookup needs no key. Censys uses CENSYS_PAT, Shodan uses SHODAN_API_KEY, and VirusTotal uses VIRUSTOTAL_API_KEY. Provider plans and rate limits still apply. The `.env` file is loaded only when you source it as shown above; the program does not auto-load it. Google keys are not used in this edition.

## Verification

```sh
pip install pytest
python -m pytest tests -q
```

Tests use mocks, not live scans. They verify physical module removal, catalog restrictions, forbidden runner paths, HTTP destinations, GET-only lookups, TLS, redirect refusal, response size limits, fixed DNS record types, bounded website requests, no form submissions and offline JWT decoding. Dependencies have not received a full security audit.

## Project structure

```text
argus/               CLI, reviewed dispatch and bounded lookup implementations
  modules/           30 module entrypoints
  passive.py         Fixed-provider HTTP lookup client and module allowlist
  nonintrusive.py    Bounded website/DNS checks and offline decoder
tests/               Mock-based safety and behavior tests
docs/MODULES.md      Inputs and behavior for each module
.env.example         Credential placeholders only
```

See [CHANGELOG.md](CHANGELOG.md) for release notes and [RESTORATION.md](RESTORATION.md) for implementation limits. The [excluded module list](removed-modules.json) documents what is not shipped.

## Attribution

Based on [divinelabio/Argus](https://github.com/divinelabio/Argus), originally credited to Jasonxtn / Jason13. Neil customized the branding, terminal-only output, Censys PAT support and restricted record-lookup edition. Original MIT copyright and license notices are retained in LICENSE.
