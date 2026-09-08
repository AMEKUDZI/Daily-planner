from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, help_text="e.g. +233543643780, for SMS reminders")

    def __str__(self):
        return f"Profile for {self.user.username}"
