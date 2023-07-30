import os
from django.db import models
from django.utils.safestring import mark_safe

from accounts.models import User
from django.db.models import Avg, Count

from math import floor, ceil, modf

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.category_name
    
class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/brands')
    def __str__(self):
        return self.brand_title

class Colour(models.Model):
    title = models.CharField(max_length=100)
    colour_code = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.title

class Size(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

def offer_image(instanse, filename):
    upload_to = "images/Deals/"
    ext =  filename.split('.')['-1']
    #get filename
    if instanse.name:
        filename = '{}.{}'.format(instanse.name, ext)
        return os.path.join(upload_to, filename)
    
class Offer(models.Model):
    name = models.CharField(max_length=50)
    discount = models.PositiveIntegerField()
    image = models.ImageField(upload_to=offer_image, blank=True, null=True)

    def __str__(self):
        return self.name
def discount_image(instanse, filename):
    upload_to = "images/Deals/"
    ext =  filename.split('.')['-1']
    #get filename
    if instanse.name:
        filename = '{}.{}'.format(instanse.name, ext)
        return os.path.join(upload_to, filename)
    
class Discount(models.Model):
    name = models.CharField(max_length=50)
    discount = models.PositiveIntegerField()
    image = models.ImageField(upload_to= discount_image, blank=True, null=True)

    def __str__(self):
        return self.name
def deal_image(instanse, filename):
    upload_to = "images/Deals/"
    ext =  filename.split('.')['-1']
    #get filename
    if instanse.name:
        filename = '{}.{}'.format(instanse.name, ext)
        return os.path.join(upload_to, filename)
    
class Deal(models.Model):
    name = models.CharField(max_length=50)
    discount = models.PositiveIntegerField()
    image = models.ImageField(upload_to= deal_image, blank=True, null=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    product_title = models.CharField(max_length=100, unique= True)
    image = models.ImageField(upload_to='images/products/', blank =True, null= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    stock = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def save(self, *args, **kwargs):
        super(Products, self).save(*args, **kwargs)
        product_variations = ProductVariation.objects.filter(product = self)
        if product_variations.count() > 0:
            for product in product_variations:
                if product.product.on_sale:
                    discount_price = product.get_discount_price()
                    if isinstance(discount_price, float):
                        dec = modf(discount_price)[0]
                        if dec < 0.5:
                            price = floor(discount_price)
                        else:
                            price = ceil(discount_price)
                    else:
                        price = discount_price
                    product.discount_price = price
                else:
                    product.discount_price = product.price
                product.save()



    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def __str__(self):
        return self.product_title
    
class ProductVariation(models.Model):
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE )
    colour = models.ForeignKey(Colour, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products/', null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.PositiveIntegerField(null=True, blank=True)
    sell_price = models.IntegerField()

    def __str__(self):
        return self.product.product_title
    
    def get_discount_price(self):
        product = self.product
        if product.on_sale:
            if product.discount:
                percent = product.discount.discount
            elif product.deal:
                percent = product.deal.discount
            elif product.offer:
                percent = product.offer.discount
            else:
                percent = 0
            price_redu = (percent*self.price)/100
            price = self.price - price_redu
            return price
        else:
            return self.price

    def save(self, *args, **kwargs):
        self.discount_price = self.get_discount_price()
        super(ProductVariation, self).save(*args, **kwargs)
    
    def discounted_price(self):
        return ((self.price)*(self.discount))/100
    
    def sell_price(self):
        return (self.price)-(self.discounted_price)
    
    def image_tag(self):
        return mark_safe('<img src="%s" height="50" width="50" />' %(self.image.url))


class Tax(models.Model):
    tax_type = models.CharField(max_length=50)
    tax_percentage = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Tax-Percentage(%)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tax_type
    

class ReviewRating(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=100, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.subject


class WishList(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_title

