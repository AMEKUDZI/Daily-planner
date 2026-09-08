from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Activity(models.Model):
    RECURRENCE_CHOICES = [
        ('none', 'One-time'),
        ('daily', 'Daily'),
        ('weekdays', 'Weekdays only'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_time = models.TimeField(help_text="Time of day this activity should happen")
    start_date = models.DateField()
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='daily')
    is_active = models.BooleanField(default=True)

    notify_email = models.BooleanField(default=True)
    notify_sms = models.BooleanField(default=False)
    notify_in_app = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.title} @ {self.scheduled_time.strftime('%H:%M')}"

    def get_absolute_url(self):
        return reverse('dashboard')

    def is_due_today(self, today_weekday):
        """today_weekday: 0=Monday ... 6=Sunday (from date.weekday())"""
        if self.recurrence == 'daily':
            return True
        if self.recurrence == 'weekdays':
            return today_weekday < 5
        if self.recurrence == 'weekly':
            return today_weekday == self.start_date.weekday()
        if self.recurrence == 'none':
            return True  # date match handled by caller
        return False


class NotificationLog(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('in_app', 'In-app'),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='notifications')
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.activity.title} - {self.channel} - {self.sent_at:%Y-%m-%d %H:%M}"
