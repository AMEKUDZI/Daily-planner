from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display  = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_filter   = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering      = ('-date_joined',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customise admin site header
admin.site.site_header = 'Daily Planner Admin'
admin.site.site_title  = 'Daily Planner'
admin.site.index_title = 'Site Administration'
