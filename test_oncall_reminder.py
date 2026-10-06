import datetime as dt
from oncall_reminder import oncall_dates as _oncall_dates


def oncall_dates(ics, today):
    return _oncall_dates(ics, today, "Primary oncall for my-team")

ICS = b"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:1
SUMMARY:Primary oncall for my-team
DTSTART;VALUE=DATE:20261002
DTEND;VALUE=DATE:20261004
RRULE:FREQ=WEEKLY;COUNT=3
END:VEVENT
BEGIN:VEVENT
UID:2
SUMMARY:Primary oncall for my-team
DTSTART;VALUE=DATE:20261001
DTEND;VALUE=DATE:20261002
END:VEVENT
BEGIN:VEVENT
UID:3
SUMMARY:Secondary oncall for my-team
DTSTART;VALUE=DATE:20261004
DTEND;VALUE=DATE:20261005
END:VEVENT
END:VCALENDAR
"""

# Fri Oct 2 (recurring) is 3 days out from Tue Sep 29; Thu Oct 1 is the wrong weekday
assert oncall_dates(ICS, dt.date(2026, 9, 29)) == [dt.date(2026, 10, 2)]
# Oct 1: Fri Oct 2 is 1 day out
assert oncall_dates(ICS, dt.date(2026, 10, 1)) == [dt.date(2026, 10, 2)]
# Oct 2: day 1 of the Fri shift is today, Oct 3 is mid-shift, Oct 5 is nothing -> no reminder
assert oncall_dates(ICS, dt.date(2026, 10, 2)) == []
# Recurrence: Fri Oct 9 is 3 days from Oct 6; secondary oncall Sun Oct 4 ignored on Oct 1/3
assert oncall_dates(ICS, dt.date(2026, 10, 6)) == [dt.date(2026, 10, 9)]
assert oncall_dates(ICS, dt.date(2026, 10, 3)) == []
print("ok")
