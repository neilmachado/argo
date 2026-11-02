# Changelog

## 2.2.0

- Ship 30 reviewed module entrypoints; exclude 117 original module files.
- Restore useful checks through constrained implementations instead of unrestricted crawling/probing code.
- Keep website checks to one homepage or standard metadata GET per invocation.
- Use fixed-provider GET-only lookups, Censys PAT authentication, TLS verification, response-size limits and no automatic redirects or retries.
- Decode JWT headers and payloads offline without downloading keys or claiming signature verification.
- Disable automatic results, reports, run logs and disk response caches.
- Add Neil branding, startup disclaimer, module reference, contribution guidance and security documentation.
- Include 35 mock-based behavior and safety checks.

This edition is derived from the MIT-licensed Argus project. It is not the original toolkit or a claim of wholly original authorship.
