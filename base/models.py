from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField


class Store(models.Model):
    name = models.CharField(max_length=299)
    address = models.CharField(max_length=299)
    website = models.CharField(max_length=299)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=299)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory_name = models.CharField(max_length=299)

    def __str__(self):
        return f"{self.subcategory_name}"


class Products(models.Model):
    image = models.ImageField(upload_to='product_images')
    name = models.CharField(max_length=299)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ForeignKey(Products, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.products}'s {self.quantity}"
    
    def get_total_price(self):
        return self.products.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cart_item = models.ManyToManyField(CartItem)
    date_ordered = models.DateTimeField(default=timezone.now)
    ordered_on = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True)
    checkout = models.ForeignKey('CheckOut', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user}'s Orders"
    
    def get_final_price(self):
        total = 0
        for items in self.cart_item.all():
            total += items.get_total_price()
        return total


class Review(models.Model):
    name = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Products, related_name='reviews', on_delete=models.PROTECT)
    image = models.ImageField(upload_to='review_images', null=True, blank=True)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s review on {self.product}"
    

class CheckOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField(multiple=False)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Checkout Details"
    
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=299)
    amount = models.CharField(max_length=299)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user
