---
name: content-sanitizer
description: Scan files/folders for sensitive information before publishing. Use when checking repositories, skills, docs, or exports for tokens, API keys, passwords, local paths, usernames, emails, secrets, and other accidental leaks.
---

# Content Sanitizer

Run a publish-safety scan before sharing code or docs.

## Workflow

1. Run `scripts/sensitive_scan.py <target_path>`.
2. Review findings by severity:
   - `HIGH`: credentials/tokens/password-like strings.
   - `MEDIUM`: local absolute paths, emails, usernames, hostnames, account identifiers.
   - `LOW`: possible hints that still deserve review.
3. Fix findings or mark safe false positives with rationale.
4. Re-scan until no unresolved HIGH findings.

## Command

```bash
python3 scripts/sensitive_scan.py /path/to/target --json-out scan-report.json
```

## Typical publish gate

- Block release on unresolved `HIGH` findings.
- Require manual review for `MEDIUM` findings.
- Allow `LOW` with note.

## Resources

- `scripts/sensitive_scan.py`: regex-based detector and summary reporter.
- `references/rules.md`: detection scope and false-positive guidance.
