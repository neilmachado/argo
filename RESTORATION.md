# Restoration notes

25 previously excluded modules restored; 30 total. All restored entrypoints use the bounded implementation in argus/nonintrusive.py instead of the original crawling/probing implementations. 117 original module files remain excluded. See removed-modules.json for the list and README.md for the exact behavior limits.

Important changes: framing, forms, CAPTCHA, comments, pixels and embed checks inspect only the homepage. Sitemap parsing does not follow links. Technology detection does not guess platform files. Social links come only from the page, with no search-engine scraping. SPF/DMARC does not guess DKIM selectors. JWT decoding never downloads keys or validates signatures. IP/ASN lookups use a public HTTPS provider, with no local port probes. No API key values are in the release source.

The original pre-publication review describes the former full toolkit and is historical; it does not describe the current restricted implementations.
