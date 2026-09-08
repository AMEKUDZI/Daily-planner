"""
Notification senders for the daily scheduler.

Email uses Django's built-in send_mail (works with Gmail SMTP once you
set EMAIL_HOST_USER / EMAIL_HOST_PASSWORD in settings.py to a Gmail
address and an App Password).

SMS uses Africa's Talking. Install their SDK with:
    pip install africastalking
and set SMS_ENABLED = True plus your real credentials in settings.py.
Until then, SMS sends are logged to the console instead of actually sent,
so you can develop and demo without a live account.
"""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import NotificationLog

logger = logging.getLogger(__name__)


def send_email_notification(activity):
    subject = f"Reminder: {activity.title}"
    message = (
        f"Hi {activity.user.first_name or activity.user.username},\n\n"
        f"It's time for: {activity.title}\n"
    )
    if activity.description:
        message += f"\n{activity.description}\n"
    message += f"\nScheduled for {activity.scheduled_time.strftime('%H:%M')}.\n"

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [activity.user.email],
            fail_silently=False,
        )
        status = 'sent'
    except Exception:
        logger.exception('Email notification failed for activity %s', activity.pk)
        status = 'failed'

    NotificationLog.objects.create(activity=activity, channel='email', status=status)


def send_sms_notification(activity):
    message = f"Reminder: {activity.title} at {activity.scheduled_time.strftime('%H:%M')}"
    phone_number = getattr(activity.user.profile, 'phone_number', None) if hasattr(activity.user, 'profile') else None

    if not settings.SMS_ENABLED or not phone_number:
        # Dev mode: no live SMS account configured yet, or the user has no
        # phone number on file. Log it so the flow is still demonstrable.
        status = 'skipped (SMS not configured or no phone number)'
    else:
        try:
            import africastalking
            africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
            sms = africastalking.SMS
            sms.send(message, [phone_number])
            status = 'sent'
        except Exception:
            logger.exception('SMS notification failed for activity %s', activity.pk)
            status = 'failed'

    NotificationLog.objects.create(activity=activity, channel='sms', status=status)


def create_in_app_notification(activity):
    NotificationLog.objects.create(activity=activity, channel='in_app', status='sent')
