from django.db import models
from accounts.models import User

from marketplace.models import ProductVariation, Products

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length= 100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, blank=True, on_delete=models.CASCADE)
    variations = models.ManyToManyField(ProductVariation, blank=True, null=True)
    cart = models.ForeignKey(Cart, blank=True, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def single_cart_total(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.product_title
    
class Tax(models.Model):
    title = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tax = models.IntegerField()

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Tax'

    def __str__(self):
        return self.title
    
