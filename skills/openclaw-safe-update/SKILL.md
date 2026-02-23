---
name: openclaw-safe-update
description: Safely plan and execute OpenClaw upgrades with backup, staged validation, and rollback. Use when the user asks to check latest version, assess whether to upgrade, run update.run, or perform post-upgrade verification for channels (Telegram/Discord), cron, relay, and custom workflows.
---

# OpenClaw Safe Update

Run upgrades with a strict, low-risk workflow.

## Workflow

1. **Require explicit user approval for update**
   - Do not run `gateway.update.run` unless user explicitly asks to upgrade now.
   - If user asks only for assessment, stop after recommendation.

2. **Collect baseline**
   - Use `gateway(config.get)` to capture current version marker and active channel config.
   - Check latest release from GitHub API (`https://api.github.com/repos/openclaw/openclaw/releases/latest`).
   - Summarize: current vs latest + expected risk.

3. **Backup before change**
   - Run `scripts/backup_openclaw_config.sh` to snapshot `~/.openclaw-dev/openclaw.json`.
   - Report backup path before proceeding.

4. **Execute upgrade**
   - Run `gateway(update.run)` only after explicit confirmation.
   - Wait for restart completion signal.

5. **Post-upgrade regression checks**
   - Use `references/regression-checklist.md`.
   - Prioritize user-critical paths first (Discord routing, Telegram reply, cron CRUD, custom relay URLs).

6. **Rollback if broken**
   - Restore latest backup over `~/.openclaw-dev/openclaw.json`.
   - Restart gateway (`gateway(restart)` or config patch/apply restart path).
   - Re-run critical checks.

## Output Format

Return concise sections:
- Version delta
- Risk summary
- Backup created at
- Upgrade result
- Regression status (pass/fail)
- Next action (continue/rollback)

## Resources

- `scripts/backup_openclaw_config.sh`: create timestamped config backup
- `references/regression-checklist.md`: fast validation matrix after upgrade
