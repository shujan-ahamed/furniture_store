from django.contrib import admin
from django.urls import path, include
from .views import home, about
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('jet/', include('jet.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('cart/', include('carts.urls')),
    path('order/', include('orders.urls')),
    path('contact/', include('contact.urls')),
    path('analytics/', include('analytics.urls')),

    path('social_accounts/', include('allauth.urls')),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
