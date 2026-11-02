# Restoration notes

25 previously excluded modules restored; 30 total. All restored entrypoints use the bounded implementation in argo/nonintrusive.py instead of the original crawling/probing implementations. 117 original module files remain excluded. See removed-modules.json for the list and README.md for the exact behavior limits.

Important changes: framing, forms, CAPTCHA, comments, pixels and embed checks inspect only the homepage. Sitemap parsing does not follow links. Technology detection does not guess platform files. Social links come only from the page, with no search-engine scraping. SPF/DMARC does not guess DKIM selectors. JWT decoding never downloads keys or validates signatures. IP/ASN lookups use a public HTTPS provider, with no local port probes. No API key values are in the release source.

The original pre-publication review describes the former full toolkit and is historical; it does not describe the current restricted implementations.

## 2.3 interface update

The current interface has only four numbered options. Module IDs have been replaced with sequential 01–30 numbering; older IDs and command-shell examples no longer apply.

## Current release: 2.4.0

31 modules are now available. AlienVault OTX was added as module 31 for existing IP, domain and hash intelligence; the original 117 excluded module files remain excluded. The home screen has four options, while selection and run sections show only contextual prompts. Inputs may be entered directly at the run prompt.

## Current release: 2.5.0

Nine overlapping entrypoints were removed by consolidation, leaving 22 modules (01–22). These are mergers, not removal of capabilities: TXT/CAA/SPF/DMARC, ASN/server IP details, framing headers, autocomplete and integration references are available in their merged results. APIs and local sources are displayed on selection and run.
