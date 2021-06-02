from django.urls import path, include
from . import views

urlpatterns = [
    path('view/<str:api_type>/', views.schedule_view, name='schedule_view'),
    path('view/vehicle/', views.schedule_view_vehicle, name='schedule_view_vehicle'),
    # for title row in schedule view

    path('view/mobile/<str:api_type>/', views.schedule_view_mobile, name='schedule_view_mobile'),

    path('availability/', views.availability, name='availability'),
    path('availability/team/', views.availability_team, name='availability'),
    path('availability/vehicle/', views.availability_vehicle, name='availability'),

    path('jobschedule/add/', views.add_to_schedule, name='availability'),
    path('jobschedule/edit/', views.add_to_schedule, name='availability'),
    path('jobschedule/team/add/', views.add_team_to_schedule, name='add_team_to_schedule'),
    path('jobschedule/images/add/', views.add_images_to_schedule, name='add_images_to_schedule'),
    path('jobschedule/images/add/<int:file_id>/', views.add_images_to_schedule, name='add_images_to_schedule'),
    path('jobschedule/signature/add/', views.add_signature_to_schedule, name='add_signature_to_schedule'),
    path('jobschedule/comments/', views.schedule_commentAPI, name='schedule_commentAPI'),
    path('jobschedule/comments/<int:comment_id>/', views.schedule_commentAPI, name='schedule_commentAPI'),   
    path('jobschedule/view/<int:job_id>/', views.schedule_get_details, name='schedule_get_details'), 
    path('jobschedule/vehicle/add/', views.add_vehicle_to_schedule, name='add_vehicle_to_schedule'),
    path('jobschedule/delete/<int:js_id>/', views.add_to_schedule, name='availability'),
    path('incomplete/view/<str:api_type>/', views.incomplete_schedule_view, name='incomplete_schedule_view'),
    
    path('additional/vehicles/', views.additional_vehicles, name='additional_vehicles'),
    path('additional/vehicles/<int:schedule_id>/', views.additional_vehicles, name='additional_vehicles'),
]