from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

urlpatterns = [
    path('access/permission/', views.get_permission_access, name='get_permission_access'),
    path('profile/view/', views.get_profile, name='get_profile'),
    path('push-notification/key/', views.push_notification, name='push_notification'),
    path('web/push-notification/delete/<str:device_id>/', views.push_notification_key_deletion, name='push_notification_key_deletion'),
]