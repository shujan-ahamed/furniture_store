from django.urls import path
from .views import cart, add_cart, decrease_cart, remove_cart, increase_cart


urlpatterns = [
    path('', cart, name= 'cart'),
    path('add_cart/<int:product_id>/', add_cart, name= 'add_cart'),
    path('decrease_cart/', decrease_cart, name= 'decrease_cart'),
    path('increase_cart/', increase_cart, name= 'increase_cart'),
    path('remove_cart/', remove_cart, name= 'remove_cart'),
    
]