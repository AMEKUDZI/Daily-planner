from django.contrib import admin
from .models import Activity, NotificationLog


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'scheduled_time', 'recurrence', 'is_active', 'created_at')
    list_filter   = ('recurrence', 'is_active', 'notify_email', 'notify_sms', 'notify_in_app')
    search_fields = ('title', 'user__username', 'user__email')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at',)
    list_per_page = 25


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display  = ('activity', 'channel', 'status', 'is_read', 'sent_at')
    list_filter   = ('channel', 'status', 'is_read')
    search_fields = ('activity__title', 'activity__user__username')
    ordering      = ('-sent_at',)
    readonly_fields = ('sent_at',)
    list_per_page = 50
