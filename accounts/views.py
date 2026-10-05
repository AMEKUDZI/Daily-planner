from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .forms import SignUpForm, ProfileForm
from .models import Profile


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Profile.objects.create(user=user, phone_number=form.cleaned_data.get('phone_number', ''))
            _send_verification_email(request, user)
            messages.info(request, 'Check your email to verify your account before signing in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def _send_verification_email(request, user):
    uid   = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link  = request.build_absolute_uri(f'/accounts/verify/{uid}/{token}/')
    send_mail(
        'Verify your Daily Planner account',
        f'Hi {user.username},\n\nClick the link below to verify your account:\n\n{link}\n\nThis link expires in 24 hours.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )


def verify_email(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email verified! You can now sign in.')
    else:
        messages.error(request, 'Verification link is invalid or has expired.')
    return redirect('login')


@login_required
def profile(request):
    instance, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=instance, user=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
