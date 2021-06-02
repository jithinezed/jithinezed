from django.urls import path, include
from . import views

urlpatterns = [
    path('view/<str:api_type>/<int:year>/<int:page_number>/', views.home_view, name='home_view'),
    path('view/weather_report/', views.weather_report, name='weather_report'),
   
]
