from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Products)
admin.site.register(models.Orders)
admin.site.register(models.Shipping_Details)
admin.site.register(models.Products_Ordered)
