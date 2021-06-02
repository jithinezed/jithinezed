from django.urls import path, include
from . import views

urlpatterns = [
    path('view/<str:api_type>/', views.job_view, name='jon_view_api'),
    path('edit/', views.job_edit_api, name='job_edit_api'),
    path('card/<int:job_id>/', views.job_card_view, name='job_card_view'),

    path('previous/sale/<int:client_id>/', views.get_previous_sale, name='get_previous_sale'),
    path('search/<str:tab_type>/', views.job_search, name='job_search'),
    path('filter/price/range/<str:tab_type>/', views.filterby_price_range, name='filterby_price_range'),
    path('manager/status-change/<str:schedule_status>/<int:job_id>/', views.ready_for_schedule_status, name='ready_for_schedule_status'),
    path('filter/<str:tab_type>/<str:filter_type>/', views.filterby_client_name, name='filterby_client_name'),  
    path('search/site/<str:tab_type>/',views.job_search_by_client_id, name=' job_search_by_client_id'), 
    path('custom/card/<int:quote_id>/',views.custom_job_card, name='custom_job_card'), 

    #april16
    path('card/info/create/',views.create_job_card_info, name='create_job_card_info'), 
    path('card/info/edit/<job_card_id>/',views.create_job_card_info, name='create_job_card_info'), 
    path('card/info/delete/<job_card_id>/',views.create_job_card_info, name='create_job_card_info'), 
    path('card/info/view/',views.create_job_card_info, name='create_job_card_info'), 

    # get job card by quote
    path('card/info/view/<quote_id>/',views.get_job_card_by_quote, name='get_job_card_by_quote'), 
    path('card/info/view/client_id/<int:client_id>/',views.get_job_card_by_client, name='get_job_card_by_quote'), 

]


