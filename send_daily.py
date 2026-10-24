"""Send one bootcamp lesson per day by email. Standard library only."""
import os, sys, smtplib, html
from datetime import date, datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path

# Lesson order: 7, 8, 9, 10, then 1..6, then the bonus file. Then it repeats.
ORDER = ["day07", "day08", "day09", "day10",
         "day01", "day02", "day03", "day04", "day05", "day06",
         "day11_bonus"]

# Link added to every email. Change here if it ever changes.
LINK_TITLE = "LLM Generative AI 10 days bootcamp"
LINK_URL = "https://chatgpt.com/share/6add096f-7bf8-83ec-b17d-377db0bdd752"

CONTENT = Path(__file__).parent / "content"
IST = timezone(timedelta(hours=5, minutes=30))


def todays_index(start: date) -> int:
    today = datetime.now(IST).date()
    return (today - start).days % len(ORDER)


def build_message(name: str, sender: str, to: str, n: int) -> EmailMessage:
    text = (CONTENT / f"{name}.txt").read_text(encoding="utf-8")
    title = text.strip().splitlines()[1] if name != "day11_bonus" else "Bonus: DevMind project, notes, glossary"
    msg = EmailMessage()
    msg["Subject"] = f"AI Bootcamp ({n + 1}/{len(ORDER)}): {title}"
    msg["From"], msg["To"] = sender, to
    msg.set_content(f"{LINK_TITLE}: {LINK_URL}\n\n{text}")
    msg.add_alternative(
        "<html><body>"
        f"<p style=\"font-family:Arial,sans-serif;font-size:15px\">&#128279; "
        f"<a href=\"{LINK_URL}\">{html.escape(LINK_TITLE)}</a></p><hr>"
        "<pre style=\"font-family:Consolas,monospace;font-size:14px;"
        f"white-space:pre-wrap;line-height:1.5\">{html.escape(text)}</pre></body></html>",
        subtype="html")
    return msg


def main() -> None:
    dry = "--dry-run" in sys.argv
    start = date.fromisoformat(os.environ.get("START_DATE", "2026-10-26"))
    if not os.environ.get("FORCE_INDEX") and datetime.now(IST).date() < start:
        print(f"Start date {start} not reached yet; nothing to send.")
        return
    n = int(os.environ["FORCE_INDEX"]) if os.environ.get("FORCE_INDEX") else todays_index(start)
    name = ORDER[n]

    sender = os.environ.get("GMAIL_ADDRESS", "me@example.com")
    to = os.environ.get("TO_EMAIL", sender)
    msg = build_message(name, sender, to, n)

    if dry:
        print(msg["Subject"]); print(msg.get_body(("plain",)).get_content()[:300]); return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(sender, os.environ["GMAIL_APP_PASSWORD"])
        s.send_message(msg)
    print("Sent:", msg["Subject"])


if __name__ == "__main__":
    main()