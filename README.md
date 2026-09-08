# Daily Planner — Final Year Project

A full-stack web app for scheduling daily activities and getting reminders
by email, SMS, and in-app notification.

- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Backend:** Python / Django
- **Database:** SQLite (default, easy to switch to PostgreSQL later)
- **Scheduler:** APScheduler (via django-apscheduler) — checks every minute for due activities
- **Email:** Django's `send_mail` (Gmail SMTP)
- **SMS:** Africa's Talking (Ghana-friendly SMS gateway)

## Project layout

```
dailyplanner/
├── manage.py
├── requirements.txt
├── scheduler_project/     # project settings, urls
├── accounts/               # signup/login/logout, user Profile (phone number)
├── activities/             # Activity model, scheduler, notifications, dashboard
├── templates/               # HTML templates
└── static/                  # CSS + JS
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — you'll be redirected to sign up / log in.

## Turning on real email

In `scheduler_project/settings.py`:

1. Set `EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`
2. Set `EMAIL_HOST_USER` to your Gmail address
3. Set `EMAIL_HOST_PASSWORD` to a **Gmail App Password** (not your normal password —
   generate one at https://myaccount.google.com/apppasswords, requires 2-Step
   Verification to be turned on)

Until you do this, reminder emails print to the console instead of sending —
useful for development and for demoing without spamming a real inbox.

## Turning on real SMS (Africa's Talking)

1. `pip install africastalking`
2. Create a free sandbox account at https://africastalking.com
3. In `settings.py`, set `SMS_ENABLED = True` and fill in
   `AFRICASTALKING_USERNAME` / `AFRICASTALKING_API_KEY`
4. Make sure each user has a `phone_number` on their `Profile` (collected at signup)

## How the scheduler works

`activities/scheduler.py` runs a background job every minute
(`check_due_activities`). It looks for activities whose `scheduled_time`
matches the current minute and whose recurrence rule (`daily`, `weekdays`,
`weekly`, `one-time`) matches today. For each match it fires whichever
channels are enabled on that activity (email / SMS / in-app) and logs the
result to `NotificationLog`, so nothing gets sent twice in the same day.

The scheduler only starts when you run `python manage.py runserver` — it's
skipped during `migrate`, `makemigrations`, etc.

## Suggested next steps for the report/demo

- Add a calendar/week view in addition to the daily timeline
- Add password reset (Django has this built in via `django.contrib.auth.views`)
- Deploy to Render, Railway, or PythonAnywhere for the live demo link
- Write unit tests for `Activity.is_due_today()` and the notification senders
