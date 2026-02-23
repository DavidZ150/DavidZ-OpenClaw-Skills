# AGENT_GUIDE.md

## Purpose
This repository provides a safety-first OpenClaw update skill.

## Intended Agent Role
- Primary: Operations/SRE-style assistant
- Secondary: General assistant handling upgrade requests

## Trigger Conditions
Use this skill when user asks to:
- Check latest OpenClaw version
- Decide whether to upgrade now
- Execute `update.run`
- Validate post-upgrade behavior

## Hard Safety Rules
1. Never run update automatically.
2. Require explicit user confirmation before `gateway.update.run`.
3. Always create config backup before upgrade.
4. If critical checks fail, recommend rollback immediately.
5. Do not expose secrets from config in user-visible output.

## Required Output Sections
- Version delta (current vs latest)
- Risk summary
- Backup path
- Upgrade result
- Regression check status
- Next action (continue/rollback)

## Regression Priorities
1. User primary messaging channel works
2. Discord/Telegram routing rules still intact
3. Cron list/add/update/delete works
4. Relay/custom endpoints still healthy

## Rollback Trigger
Any of the following should trigger rollback recommendation:
- Primary channel cannot send/receive
- Cron CRUD broken
- Config critical sections missing/reset
