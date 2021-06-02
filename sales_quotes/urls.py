from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [

    path('quote/<str:tab_type>/<int:page>/', views.send_quote, name='send_quote'),
    path('quote/<str:tab_type>/', views.send_quote, name='send_quote'),
    path('performance/<str:tab_type>/', views.re_sale_performance, name='re_sale_performance'),
    path('performance/<str:tab_type>/<int:year>/<int:month>/', views.re_performance_filter, name='re_performance_filter'),
    path('performance/<str:tab_type>/<int:year>/', views.re_performance_filter, name='re_performance_filter'),
    path('jobs/<str:tab_type>/<int:page_number>/', views.re_generated_jobs, name='re_generated_jobs'),
    path('jobs/<str:tab_type>/', views.re_generated_jobs, name='re_generated_jobs'),
    path('job/<str:tab_type>/<int:job_id>/', views.re_get_job_details, name='re_get_job_details'),
    path('manager/<str:tab_type>/<int:manager_id>/<int:page_number>/', views.re_manager_quotes, name='re_manager_quotes'),
    path('manager/<str:tab_type>/<int:manager_id>/', views.re_manager_quotes, name='re_manager_quotes'),

    path('jobs/filter/<str:tab_type>/<str:payment>/<int:page>/', views.re_job_filter_byPayment, name='re_job_filter_byPayment'),
    path('jobs/filter/<str:tab_type>/<str:payment>/', views.re_job_filter_byPayment, name='re_job_filter_byPayment'),
    
    #  path('folder/list/<str:tab_type>/<str:sales_archive>/', views.re_get_sales_folders_and_files, name='re_get_sales_folders_and_files'),

    path('folders/generate_quote/<str:tab_type>/', views.re_get_generate_quote_folder_list, name='re_get_generate_quote_folder_list'),
    path('folders/quote_attachments/<str:tab_type>/',views.re_get_generate_quote_folder_attachment, name='re_get_generate_quote_folder_attachment'),

    path('client/status/<str:status>/<str:quote_id>/', views.client_quote_status, name='client_quote_status'),
    path('quote/manager/<str:status_change>/<int:quote_id>/', views.quote_status_change, name='quote_status_change'),
    path('client/quote/<str:quote_id>/', views.client_view_quote, name='client_view_quote'), 
    path('search/quote/<str:tab_type>/',views.quote_search, name='quote_search'), 
    path('quote/resent/mail/<str:tab_type>/<int:quote_id>/',views.resent_quote_mail, name='resent_quote_mail'),    
    path('quote/price/range/<str:tab_type>/',views.filterby_price_range, name='filterby_price_range'), 
    path('quote/price/range/<str:tab_type>/',views.filterby_price_range, name='filterby_price_range'),
    path('products/<int:product_id>/',views.products, name='products'),
    path('products/',views.products, name='products'),
    path('user/quote/template/<str:tab_type>/',views.user_qoute_template, name='user_qoute_template'),  
    path('single/user/quote/template/<int:template_id>/',views.single_user_qoute_template, name='single_user_qoute_template'),   
    path('user/template/draft/<str:tab_type>/',views.draft_template, name='draft_template'), 

   
    path('user/template/draft/<str:tab_type>/<int:client_id>/',views.draft_template, name='draft_template'), 
    path('single/template/draft/<int:draft_id>/',views.single_draft_template, name='single_draft_template'), 

    path('template/draft/all/<str:tab_type>/',views.get_all_draft_template, name='get_all_draft_template'), 

    path('user/quote/safety_data/<str:tab_type>/<int:employee_id>/',views.user_safety_data, name='user_safety_data'),  
    path('single/user/quote/safety_data/<int:safety_data_id>/',views.single_user_safety_data, name='single_user_safety_data'),  
    path('filter/site-date/<str:tab_type>/<str:search_key>/<int:page>/',views.quote_search_date_site_client, name='quote_search_date_site_client'),  
    path('filter/site-date/<str:tab_type>/<str:search_key>/',views.quote_search_date_site_client, name='quote_search_date_site_client'),
    path('filter/site-date/<str:tab_type>/<str:search_key>/',views.quote_search_date_site_client, name='quote_search_date_site_client'),
    #this url for get 8 templates id and get sigle template html code and alse can post  edited template
    path('quote/attach/templates/<str:tab_type>/<int:template_id>/',views.quote_attach_templates, name='quote_attach_templates'), 
    path('quote/attach/templates/<str:tab_type>/',views.quote_attach_templates, name='quote_attach_templates'),

    path('quote/<str:tab_type>/filterby/status/<str:state>/<int:manager_id>/<int:page_number>/',views.quote_filter_by_state, name='quote_filter_by_state'), 
    path('quote/<str:tab_type>/filterby/status/<str:state>/<int:manager_id>/',views.quote_filter_by_state, name='quote_filter_by_state'),
    path('waste/type/<int:w_id>/',views.type_of_waste, name=' type_of_waste'), 
    path('waste/type/',views.type_of_waste, name=' type_of_waste'), 
    path('quote/client/search/',views.Quote_client_search, name=' Quote_client_search'), 

    path('jobs/ready/list/<str:tab_type>/<int:page_number>/',views.Ready_for_scheduled_jobs, name=' Ready_for_scheduled_jobs'), 
    path('jobs/ready/list/<str:tab_type>/',views.Ready_for_scheduled_jobs, name=' Ready_for_scheduled_jobs'), 
    path('quote/search/site/<str:tab_type>/',views.quote_search_by_client_id, name=' quote_search_by_client_id'), 
    path('quote/sales-team/<str:status>/<int:quote_id>/',views.sales_team_review_status, name=' sales_team_review_status'), 
    path('Logging/details/view/<int:quote_id>/',views.Logging_details, name=' Logging_details'), 
    path('quote/client/response/files/<str:quote_id>/',views.client_quote_attachment_response, name=' client_quote_attachment_response'),
    path('folder/<str:sales_tab>/create/',views.sales_folder_update, name=' sales_folder_update'), 
   
   path('folder/list/<str:sales_archive>/<int:folder_id>/', views.re_get_sales_folders_and_files, name='re_get_sales_folders_and_files'),

   #this api for debug server queries
    path('debugging/query/test/',views.debug_query_for_testing, name='debug_query_for_testing')
]