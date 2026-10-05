from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('activity/add/', views.add_activity, name='add_activity'),
    path('activity/<int:pk>/edit/', views.edit_activity, name='edit_activity'),
    path('activity/<int:pk>/delete/', views.delete_activity, name='delete_activity'),
    path('activity/<int:pk>/toggle/', views.toggle_active, name='toggle_active'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),
]
