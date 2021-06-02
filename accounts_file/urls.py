from django.urls import path, include
from . import views

urlpatterns = [
    path('drive/',include('drive.urls')),
    path('folder/segment/list/<int:folder_id>/', views.folder_segment_list, name='folder_segment_list'),
    path('folder/create/', views.accounts_folder_update, name='accounts_folder_update'),
]
