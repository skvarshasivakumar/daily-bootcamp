# Daily AI Bootcamp Email

Sends one lesson per day, in this order: Day 7, 8, 9, 10, then 1, 2, 3, 4, 5, 6, then a Bonus
(DevMind project + notes + glossary), then it starts again.

## Tech stack
| Need | Choice |
|---|---|
| Language | Python 3 (standard library only, nothing to pip install) |
| Email | Gmail SMTP + App Password |
| Scheduler | GitHub Actions cron (free, no server) |
| Content | Plain .txt files in `content/` |

## Setup (about 10 minutes)
1. Gmail: turn on 2-Step Verification, then create an App Password at https://myaccount.google.com/apppasswords
2. Create a GitHub repo and push this folder to it (keep it **private**).
3. Repo > Settings > Secrets and variables > Actions:
   - Secrets: `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`, `TO_EMAIL`
   - Variable: `START_DATE` (e.g. `2026-10-26`; the day Day 7 should arrive)
4. Actions tab > "Daily bootcamp email" > Run workflow, to test.
5. Done. It now runs every day at 7:00 AM IST. Change the cron line to change the time.

## Test locally
    python send_daily.py --dry-run                 # print today's email
    FORCE_INDEX=3 python send_daily.py --dry-run   # preview any lesson (0-10)
    # real send: set the env vars from .env.example, then run without --dry-run
