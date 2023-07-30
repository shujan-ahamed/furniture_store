from django.urls import path
from .views import sales_ajax_data, sales_data

urlpatterns = [
    path('sales_data/', sales_data, name= 'sales_data'),
    path('sales_ajax_data/', sales_ajax_data, name= 'sales_ajax_data'),
    
]