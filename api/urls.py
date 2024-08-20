from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateProduct.as_view(), name='create_product'),
    path('products/', views.GetProducts.as_view(), name='get_product')
]