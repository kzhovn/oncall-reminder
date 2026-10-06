"""DM a Discord user when a Tue/Fri/Sun oncall shift is 1 or 3 days away. Run once daily (cron)."""
import datetime as dt
import json
import os
import urllib.request

import icalendar
import recurring_ical_events

WEEKDAYS = {1, 4, 6}  # Tue, Fri, Sun
LEADS = (1, 3)


def oncall_dates(ics, today, prefix):
    """Oncall start dates exactly 1 or 3 days after `today` that fall on a watched weekday."""
    cal = recurring_ical_events.of(icalendar.Calendar.from_ical(ics))
    hits = set()
    for lead in LEADS:
        day = today + dt.timedelta(days=lead)
        for ev in cal.at(day):
            if not str(ev.get("SUMMARY", "")).startswith(prefix):
                continue
            start = ev["DTSTART"].dt
            if isinstance(start, dt.datetime):
                start = start.astimezone().date()  # compare in this machine's local tz
            # .at() also returns multi-day shifts that began earlier; only remind on the start day
            if start == day and start.weekday() in WEEKDAYS:
                hits.add(start)
    return sorted(hits)


def discord(path, body):
    req = urllib.request.Request(
        "https://discord.com/api/v10" + path,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bot {os.environ['DISCORD_BOT_TOKEN']}",
            "Content-Type": "application/json",
            # Discord's Cloudflare rejects the default urllib UA
            "User-Agent": "DiscordBot (oncall-reminder, 1.0)",
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    with urllib.request.urlopen(os.environ["CALENDAR_ICS_URL"]) as r:
        dates = oncall_dates(r.read(), dt.date.today(), os.environ["EVENT_PREFIX"])
    print(f"{dt.datetime.now():%Y-%m-%d %H:%M} reminders: {[str(d) for d in dates]}", flush=True)
    if not dates:
        return
    channel = discord("/users/@me/channels", {"recipient_id": os.environ["DISCORD_USER_ID"]})
    for d in dates:
        discord(f"/channels/{channel['id']}/messages", {"content": f"{os.environ['ONCALL_NAME']} is oncall {d:%a %b} {d.day}"})


if __name__ == "__main__":
    main()
