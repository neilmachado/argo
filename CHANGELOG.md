# Changelog

## 2.4.0

- Add module 31: AlienVault OTX Threat Intelligence for IP, domain and file-hash indicator records.
- Require a private OTX_API_KEY; use only the existing-indicator general GET endpoint.
- Preserve bounded HTTP safeguards, input validation and contextual navigation.
- Make menu numbering limits dynamic.
- Include 80 mock-based checks; authenticated OTX lookup verified locally with a private key.

## 2.3.1

- Accept target input directly at the ready/results prompt, preserving token case.

- Show the four-option menu only on the home screen.
- Keep selection and results in their own context with Enter to run, b for home and q to exit.
- Remove unrelated global-menu instructions from module details.
- Verify contextual navigation with 55 automated checks.

## 2.3.0

- Replace the command shell with four choices: view, select, run, exit.
- Renumber modules 01–30 with no gaps.
- Show required input, example and credential status at selection.
- Prompt for fresh input on every run and validate it before network access.
- Preserve explicit HTTP schemes and JWT tokens without the old command parser.
- Include 51 mock-based checks covering the guided flow and existing network boundaries.

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
