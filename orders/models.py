from django.db import models
from accounts.models import User

from marketplace.models import Products
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum, Avg, Count


import datetime
from django.utils import timezone

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    ammount_paid = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('paid', 'paid'),
        ('Cancelled', 'Cancelled'),
        ('refunded', 'refunded'),
        ('shipped', 'shipped'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    order_subtotal = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    payment_method = models.CharField(blank=True, max_length=20, null=True)
    shipping_method = models.CharField(max_length=100, null=True, blank=True)
    shipping_cost = models.PositiveIntegerField(null=True, blank=True)
    tax_data = models.JSONField(blank=True, null=True, help_text="Data format : {'tax_type: {'tax_percentage: 'tax_amount'}}")
    total_tax = models.FloatField()
    coupon = models.ForeignKey('Coupon', null=True, blank=True, on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name
    
    def by_week_range(self, week_ago, number_of_weeks):
        day_ago_start = week_ago * 7
        day_ago_end = week_ago - (number_of_weeks * 7 )

        now = timezone.now()
        print(';',now)

        start_date = now - datetime.timedelta(days=day_ago_start)
        end_date = now -  datetime.timedelta(days=day_ago_end)
        return self.by_range(start_date, end_date = end_date)
    
    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated_at__gte = start_date)
        return self.filter(updated_at__gte = start_date, updated_at__lte = end_date)

    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_product')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    invoice_numr = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    product_size = models.CharField(max_length=100, blank=True, null=True)
    product_colour = models.CharField(max_length=100, blank=True, null=True)
    product_image_url = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.FloatField()
    ordered = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_title
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

class Shipping(models.Model):
    method = models.CharField(max_length=50, unique=True)
    cost = models.PositiveIntegerField()
    delivery_days_min = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    delivery_days_max = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(30)])
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.method