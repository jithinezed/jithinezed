from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    path('slots/<str:date>/', views.getRoaster, name='getRoaster'),
    path('slot/<int:roaster_id>/<str:date>/', views.getRoasterById, name='getRoasterById'),
    path('create/', views.createRoaster, name='createRoaster'),
    path('report/<str:date>/', views.weaklyReport, name='weaklyReport'),

            


]