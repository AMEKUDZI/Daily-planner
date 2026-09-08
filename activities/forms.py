from django import forms
from .models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'scheduled_time', 'start_date',
            'recurrence', 'notify_email', 'notify_sms', 'notify_in_app',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Morning study session'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
