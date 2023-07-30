from django.urls import path
from .views import place_order, payment, order_complete, order_details, coupon_apply

urlpatterns = [
    path('place_order/', place_order, name= 'place_order'),
    path('payment/', payment, name= 'payment'),
    path('order_complete/', order_complete, name= 'order_complete'),
    path('order_details/<int:order_number>', order_details, name= 'order_details'),

    path('coupon_apply/', coupon_apply, name= 'coupon_apply'),


]