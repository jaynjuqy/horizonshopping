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