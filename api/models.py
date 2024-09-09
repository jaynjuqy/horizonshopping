from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Products(models.Model):
    Seller = models.ForeignKey(User, on_delete=models.CASCADE)
    Image = CloudinaryField('image')
    Name = models.CharField(max_length=400)
    Description = models.CharField(max_length=10000)
    Category = models.CharField(max_length=20)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Sold = models.BooleanField(default=False)

class Shipping_Details(models.Model):
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=15)
    town = models.CharField(max_length=30)
    apartment = models.CharField(max_length=30)
    contact = models.IntegerField()
    delivery_method = models.CharField(max_length=100)

class Orders(models.Model):
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    shipped_status = models.BooleanField(default=False)
    delivery_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Products_Ordered(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


