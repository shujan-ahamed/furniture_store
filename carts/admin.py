from django.contrib import admin

from carts.models import Cart, CartItem, Tax

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Tax)