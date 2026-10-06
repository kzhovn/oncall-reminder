# oncall-reminder

Sends a Discord DM 3 days and 1 day before any Google Calendar event whose title starts with
`EVENT_PREFIX` and that starts on a Tuesday, Friday or Sunday: "`ONCALL_NAME` is oncall Fri Oct 30".

## Setup (Debian/Ubuntu VM)

```sh
sudo apt install python3-venv git
git clone https://github.com/kzhovn/oncall-reminder ~/oncall-reminder
cd ~/oncall-reminder
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env && chmod 600 .env   # then fill it in
```

- `CALENDAR_ICS_URL`: Google Calendar → calendar settings → "Secret address in iCal format".
- `DISCORD_BOT_TOKEN`: from discord.com/developers. The bot must share a server with the recipient.
- `DISCORD_USER_ID`: Discord Developer Mode → right-click the user → Copy User ID.

Check it works (this sends a DM if a shift is 1 or 3 days away):

```sh
set -a; . ./.env; set +a; .venv/bin/python oncall_reminder.py
```

Run daily at 9am via `crontab -e`. Run it only once a day, or reminders get sent twice:

```
0 9 * * * cd ~/oncall-reminder && set -a && . ./.env && .venv/bin/python oncall_reminder.py
```

Times are compared in the VM's local timezone, so set it to match the calendar (`sudo timedatectl set-timezone ...`).

## Test

```sh
.venv/bin/python test_oncall_reminder.py
```
