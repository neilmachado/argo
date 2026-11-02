# Contributing

Thank you for helping improve Argo.

## Development

Use Python 3.10 or newer and a virtual environment:

```sh
pip install -e '.[dev]'
python -m pytest tests -q
```

Keep changes focused. Describe the behavior change and include relevant test results in the pull request.

## Scope

The project supports public-record lookups, bounded ordinary DNS queries, offline analysis and limited website inspection. Do not introduce port/range scans, credential guessing, fuzzing, bypass payloads, secret-file discovery, mutation requests, or external scan submissions.

Website checks must use the shared bounded client: one homepage/standard-metadata GET per invocation, TLS verification enabled, no redirects, no crawling, no scripts or form submissions, finite timeouts and response-size limits. Do not add another network client to bypass these constraints. DNS queries must remain fixed and bounded.

Test with mocks or systems you own and are authorized to assess. Never include live API keys, personal tokens, target exports or sensitive page contents in commits, logs, fixtures or issues.

Retain the upstream MIT notice and distinguish original code from modifications. Report security issues using the guidance in SECURITY.md.
