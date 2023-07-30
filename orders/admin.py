from django.contrib import admin
from .models import Coupon, Order, OrderProduct, Payment, Shipping

# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'quantity', 'product_price','ordered']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','full_name','email', 'phone', 'full_address', 'order_total', 'tax_data', 'status', 'is_ordered','updated_at', 'created_at')
    list_filter = ('status','is_ordered')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'order_number')
    list_per_page = 20
    inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('invoice_numr','order','payment','user', 'product', 'quantity', 'product_price', 'product_size', 'product_colour', 'total_amount', 'ordered', 'created_at')
    

class CouponAdmin(admin.ModelAdmin):
    list_display = ('id','code','valid_from','valid_to', 'discount', 'active')
    list_filter = ('active','valid_from','valid_to')
    search_fields = ('code',)

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id','method','cost','delivery_days_min', 'delivery_days_max', 'available')
    list_filter = ('available',)
    search_fields = ('method',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Shipping, ShippingAdmin)