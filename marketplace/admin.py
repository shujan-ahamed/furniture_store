from django.contrib import admin
from .models import Brand, Category, Colour, Deal, Discount, Offer, ProductVariation, Products, ReviewRating, Size, Tax, WishList

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'created_at']
    prepopulated_fields = {'slug': ('category_name',)}

class ProductsAdmin(admin.ModelAdmin):
    list_display = ['product_title', 'price', 'stock', 'created_at', 'is_available']
    prepopulated_fields = {'slug': ('product_title',)}
    list_editable = ['is_available']

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'product', 'colour', 'size', 'price', 'discount_price']
    readonly_fields=('discount_price',)

    #discount price field is directly connected to models . that means its not depended to products rather to product
admin.site.register(Brand)
admin.site.register(Colour)
admin.site.register(Size)


admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(Category, CategoryAdmin)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    '''Admin View for Tax'''

    list_display = ('tax_type', 'tax_percentage', 'is_active')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','subject', 'review', 'rating']

admin.site.register(ReviewRating, ReviewRatingAdmin)

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','created_at']

admin.site.register(WishList, WishListAdmin)

admin.site.register(Offer)
admin.site.register(Discount)
admin.site.register(Deal)
