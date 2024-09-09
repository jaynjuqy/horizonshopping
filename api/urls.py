from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateProduct.as_view(), name='create_product'),
    path('products/', views.GetProducts.as_view(), name='get_product'),
    path('paypal/create/', views.CreatePayment.as_view(), name="create_payment"),
    path('paypal/execute/', views.execute_payment, name="execute_payment"),
    path('paypal/cancel/', views.cancel_payment, name="cancel_payment"),
    path('shipping_details/', views.CreateShipmentDetails.as_view(), name='shipping_details'),
    path('orders/', views.CreateOrder.as_view(), name='order'),
    path('orderdetails/', views.Order_Details.as_view(), name='order_details'),
]