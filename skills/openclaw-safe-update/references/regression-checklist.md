# Regression Checklist (Post-Upgrade)

## A. Core health
- [ ] Gateway restart completed
- [ ] `gateway(config.get)` returns valid config
- [ ] Current version reflects expected update

## B. Messaging paths
- [ ] Telegram direct reply works
- [ ] Discord private channel reply works
- [ ] Discord routing rules still work (sticky @ rule, if configured)

## C. Automation
- [ ] `cron(list)` works
- [ ] Add/update/delete test job works
- [ ] Existing critical jobs still present

## D. Custom project paths
- [ ] Cron Studio URL still reachable
- [ ] Relay health endpoint returns OK (if used)
- [ ] Any custom systemPrompt/channel policy still present

## E. Rollback criteria (trigger rollback if any)
- [ ] Message delivery broken on primary channel
- [ ] Cron CRUD broken
- [ ] Critical config sections missing or reset unexpectedly
