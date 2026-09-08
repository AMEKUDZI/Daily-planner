from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone

from .models import Activity, NotificationLog
from .notifications import (
    send_email_notification,
    send_sms_notification,
    create_in_app_notification,
)


def check_due_activities():
    """Runs every minute. Finds activities due right now and fires
    whichever notification channels each one has enabled."""
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)
    weekday = now.weekday()
    today = now.date()

    candidates = Activity.objects.filter(
        is_active=True,
        scheduled_time__hour=current_time.hour,
        scheduled_time__minute=current_time.minute,
        start_date__lte=today,
    )

    for activity in candidates:
        if activity.recurrence == 'none' and activity.start_date != today:
            continue
        if not activity.is_due_today(weekday):
            continue

        already_sent_today = NotificationLog.objects.filter(
            activity=activity, sent_at__date=today
        ).exists()
        if already_sent_today:
            continue

        if activity.notify_email and activity.user.email:
            send_email_notification(activity)
        if activity.notify_sms:
            send_sms_notification(activity)
        if activity.notify_in_app:
            create_in_app_notification(activity)


def start():
    scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        check_due_activities,
        trigger='interval',
        minutes=1,
        id='check_due_activities',
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
