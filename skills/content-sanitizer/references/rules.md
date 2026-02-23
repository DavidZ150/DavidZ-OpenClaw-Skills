# Sensitive Scan Rules

## HIGH
- API keys and tokens (`sk-`, `xoxb-`, `ghp_`, `AKIA...`, bearer tokens)
- Password assignments (`password =`, `passwd:` etc.)
- Private key blocks

## MEDIUM
- Absolute local paths (`/Users/...`, `/home/...`, `C:\Users\...`)
- Email addresses
- Hostnames and machine names (`*.local`, device hostnames)
- Account IDs and bot tokens in config-like files

## LOW
- Generic words like `secret`, `token`, `credential` without obvious value

## Notes
- Regex scanning can produce false positives.
- Always manually inspect findings near the matched lines.
