from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count

from .models import Activity, NotificationLog
from .forms import ActivityForm


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


@login_required
def dashboard(request):
    activities = Activity.objects.filter(user=request.user).order_by('scheduled_time')
    active_count = activities.filter(is_active=True).count()
    notifications = NotificationLog.objects.filter(
        activity__user=request.user, channel='in_app'
    ).order_by('-sent_at')[:10]
    unread_count = NotificationLog.objects.filter(
        activity__user=request.user, channel='in_app', is_read=False
    ).count()

    context = {
        'activities': activities,
        'active_count': active_count,
        'notifications': notifications,
        'unread_count': unread_count,
        'today': timezone.localdate(),
    }
    return render(request, 'activities/dashboard.html', context)


@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, f'"{activity.title}" was scheduled.')
            return redirect('dashboard')
    else:
        form = ActivityForm(initial={'start_date': timezone.localdate()})
    return render(request, 'activities/activity_form.html', {'form': form, 'mode': 'Add'})


@login_required
def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{activity.title}" was updated.')
            return redirect('dashboard')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'activities/activity_form.html', {'form': form, 'mode': 'Edit', 'activity': activity})


@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        title = activity.title
        activity.delete()
        messages.success(request, f'"{title}" was removed.')
        return redirect('dashboard')
    return render(request, 'activities/activity_confirm_delete.html', {'activity': activity})


@login_required
def toggle_active(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    activity.is_active = not activity.is_active
    activity.save()
    return redirect('dashboard')


@login_required
def mark_notifications_read(request):
    if request.method != 'POST':
        return redirect('dashboard')
    NotificationLog.objects.filter(activity__user=request.user, is_read=False).update(is_read=True)
    return redirect('dashboard')
