# Security policy

## Supported version

Security changes target the current 2.2.x edition. The original unrestricted Argus toolkit is outside this project's release scope.

## Reporting a vulnerability

Do not post API keys, tokens, private targets, personal data, or working exploit details in a public issue. If this repository has GitHub private vulnerability reporting enabled, use its Security tab. Otherwise open a minimal issue requesting a private reporting channel, without disclosing sensitive details.

Include the affected version, module, expected behavior, actual behavior, and a minimal mocked or local reproduction. No response-time commitment is implied.

## Boundaries and limitations

Website checks generate low-impact active traffic and require authorization. DNS and public-record lookups also generate traffic and disclose lookup terms to providers. GET is not a universal guarantee against side effects on a misconfigured server. Hostname DNS resolution is not an ownership check or a network-isolation boundary.

The tool does not provide a legal or security certification. Header, CAPTCHA, pixel and technology findings are observations rather than proven vulnerabilities. JWT decoding does not validate signatures or trust. No saved result files does not prevent terminal scrollback, shell capture or provider logging.

Use your own provider credentials, store them outside version control, and rotate any exposed values. Dependencies have not received a comprehensive independent security audit.
