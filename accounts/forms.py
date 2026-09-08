from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


def normalise_phone(number):
    """Convert 0XXXXXXXXX to +233XXXXXXXXX for Africa's Talking."""
    n = number.strip()
    if n.startswith('0') and len(n) == 10:
        return '+233' + n[1:]
    return n


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False, help_text="e.g. 0543643780 or +233543643780")

    def clean_phone_number(self):
        number = self.cleaned_data.get('phone_number', '')
        return normalise_phone(number) if number else ''

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['phone_number']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email

    def clean_phone_number(self):
        number = self.cleaned_data.get('phone_number', '')
        return normalise_phone(number) if number else ''

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
            profile.save()
        return profile
