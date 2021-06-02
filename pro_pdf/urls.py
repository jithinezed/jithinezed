from django.urls import path
from .import views

urlpatterns = [
    path('generate_pdf/<int:template_id>/', views.generate_pdf,name='generate_pdf'),
    path('templates/', views.get_template_list,name='get_template_list'),
    path('pump/templates/', views.pump_get_template_list,name='pump_get_template_list'),
    path('download/edited/', views.download_edited_pdf,name='download_edited_pdf')
    # path('products/', views.products,name='products'),
    # path('category_list', views.category_list,name='category'),
    # path('poduct_list', views.single_product,name='single_product'),
    # path('single_category', views.single_category,name='single_category'),

    # path('pdf', views.generate_pdf, name='generate_pdf'),
]
