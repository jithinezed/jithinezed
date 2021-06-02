from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('<int:employee_id>/', views.employee_archive, name='employee_archive'),
]
