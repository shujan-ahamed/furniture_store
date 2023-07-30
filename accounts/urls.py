from django.urls import path
from .views import activate, addto_wish_list, change_password, forgot_password, login, logout, my_orders, profile, registerUser, dashboard, reset_password, reset_password_validate, wishlist


urlpatterns = [
    path('register/', registerUser, name= 'registerUser'),
    path('dashboard/', dashboard, name= 'dashboard'),
    path('my_orders/', my_orders, name= 'my_orders'),
    path('wish_list/', wishlist, name= 'wish_list'),
    path('profile/', profile, name= 'profile'),
    path('login/', login, name= 'login'),
    path('logout/', logout, name= 'logout'),
    path('activate/<uidb64>/<token>', activate, name= 'activate'),

    path('change_password/', change_password , name='change_password' ),

    path('reset_password_validate/<uidb64>/<token>/', reset_password_validate, name='reset_password_validate' ),
    path('forgot_password/', forgot_password, name='forgot_password' ),
    path('reset_password/', reset_password, name='reset_password' ),


    path('addto_wish_list/<int:product_id>', addto_wish_list, name= 'addto_wish_list'),

]