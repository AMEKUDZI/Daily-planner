from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import SignUpForm, ProfileForm
from .models import Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, phone_number=form.cleaned_data.get('phone_number', ''))
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account is ready.')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


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
