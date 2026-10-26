"""Send one bootcamp lesson + one DSA-sheet slice per day by email. Standard library only."""
import os, sys, json, smtplib, html
from datetime import date, datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path

ORDER = ["day07", "day08", "day09", "day10",
         "day01", "day02", "day03", "day04", "day05", "day06",
         "day11_bonus"]

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


def build_dsa_message(sender: str, to: str, day: int):
    """One slice of the DSA sheet. Returns None if no sheet or the plan is finished."""
    f = CONTENT / "dsa.json"
    if not f.exists():
        return None
    items = json.loads(f.read_text(encoding="utf-8"))
    per = int(os.environ.get("DSA_PER_DAY") or 8)
    total_days = -(-len(items) // per)
    if not 0 <= day < total_days:
        return None
    chunk = items[day * per:(day + 1) * per]
    first, last = chunk[0]["no"], chunk[-1]["no"]
    head = (f"Day {day + 1} of {total_days} | problems {first}-{last} of {len(items)} "
            f"| {len(items) - last} left after today")

    plain, rows, cur = [head], [f'<p style="font-family:Arial,sans-serif"><b>{html.escape(head)}</b></p>'], None
    for it in chunk:
        group = f'{it["section"]} > {it["sub"]}' if it["sub"] else it["section"]
        if group != cur:
            cur = group
            plain += ["", group.upper()]
            rows.append(f'<h3 style="font-family:Arial,sans-serif;color:#2e74b5;margin:18px 0 6px">'
                        f'{html.escape(group)}</h3>')
        plain.append(f'{it["no"]}. {it["title"]}  ' +
                     (" | ".join(f'{l["label"]}: {l["url"]}' for l in it["links"]) or "(conceptual)"))
        links = " &nbsp;".join(f'[<a href="{html.escape(l["url"])}">{html.escape(l["label"])}</a>]'
                               for l in it["links"]) or '<i style="color:#999">conceptual</i>'
        rows.append(f'<p style="font-family:Arial,sans-serif;font-size:15px;margin:6px 0">'
                    f'<b>{it["no"]}.</b> {html.escape(it["title"])} &nbsp;{links}</p>')

    msg = EmailMessage()
    msg["Subject"] = f"DSA Sheet (Day {day + 1}/{total_days}): problems {first}-{last}"
    msg["From"], msg["To"] = sender, to
    msg.set_content("\n".join(plain))
    msg.add_alternative("<html><body>" + "".join(rows) + "</body></html>", subtype="html")
    return msg


def main() -> None:
    dry = "--dry-run" in sys.argv
    start = date.fromisoformat(os.environ.get("START_DATE", "2026-10-26"))
    forced = os.environ.get("FORCE_INDEX")
    if not forced and datetime.now(IST).date() < start:
        print(f"Start date {start} not reached yet; nothing to send.")
        return
    n = int(forced) if forced else todays_index(start)
    day = int(forced) if forced else (datetime.now(IST).date() - start).days

    sender = os.environ.get("GMAIL_ADDRESS", "me@example.com")
    to = os.environ.get("TO_EMAIL", sender)
    msgs = [build_message(ORDER[n], sender, to, n)]
    dsa = build_dsa_message(sender, to, day)
    if dsa:
        msgs.append(dsa)

    if dry:
        for m in msgs:
            print(m["Subject"]); print(m.get_body(("plain",)).get_content()[:700]); print("-" * 40)
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(sender, os.environ["GMAIL_APP_PASSWORD"])
        for m in msgs:
            s.send_message(m)
            print("Sent:", m["Subject"])


if __name__ == "__main__":
    main()