from rest_framework import generics
from rest_framework.views import APIView
from . import serializers, models
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from api.paypal_config import paypalrestsdk
import logging

class CreateProduct(generics.CreateAPIView):
    queryset = models.Products.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(Seller = self.request.user)

class GetProducts(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = models.Products.objects.all()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        sort_method = self.request.query_params.get('sortby')
    
        if category:
            queryset = queryset.filter(Category=category)
        
        if search:
            queryset = queryset.filter(Q(Name__icontains=search)| Q(Description__icontains=search))
        
        if sort_method:
            if sort_method == 'lowest_price':
                queryset = queryset.order_by('Price')
            elif sort_method == 'highest_price':
                queryset = queryset.order_by('-Price')
            else:
                raise Exception("Error")
        if min_price:
            try:
                min_price = Decimal(min_price)
                queryset = queryset.filter(Price__gte=min_price)
            except(InvalidOperation, ValueError):
                print("Error: ",ValueError) 
        
        if max_price:
            try:
                max_price = Decimal(max_price)
                queryset = queryset.filter(Price__lte=max_price)
            except (InvalidOperation, ValueError):
                print("Error: ",ValueError)
                
        return queryset

class CreatePayment(APIView):
    def post(self, request, *args, **kwargs):
        total = request.data.get("total")
        if(total):
            Decimal(total)
        else:
            return JsonResponse({"Error": "Amount is missing"}, status=404)
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": total,
                    "currency": "USD",
                },
                "description": "Test Payment"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:5173/checkout/paymentok",
                "cancel_url": "http://localhost:5173/checkout/paymentcancel",
            }
        })

        if payment.create():
            return JsonResponse({"approval_url": payment['links'][1]['href']}, status=200)
        else:
            return JsonResponse({"error": payment.error}, status=400)
    
@csrf_exempt
def execute_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('paymentId')
        payer_id = data.get('PayerID')
  
    elif request.method == 'GET':
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
    if not payment_id or not payer_id:
        logging.error(f"paymentId: {payment_id} PayerID: {payer_id}")
        return JsonResponse({"error": "Missing either payment id or payer id"}, status=400)

    try:
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            return JsonResponse({"status": "Payment successful"}, status=200)
        else:
            return JsonResponse({"error": payment.error}, status=400)
    except paypalrestsdk.ResourceNotFound:
        return JsonResponse({"error": "Payment not found"}, status=404)

def cancel_payment(request):
    return JsonResponse({"status": "Payment cancelled"})

class CreateShipmentDetails(generics.CreateAPIView):
    queryset = models.Shipping_Details.objects.all()
    serializer_class = serializers.ShippingSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        buyer_id = request.data.get('buyer_id')
        if not buyer_id:
            return JsonResponse({"error": "Buyer_id is required"}, status=404)

        try:
            shipping_details = models.Shipping_Details.objects.filter(buyer_id=buyer_id).first()
            serializer = self.get_serializer(shipping_details, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": serializer.data}, status=200)
            else:
                return JsonResponse({"error": serializer.errors}, status=400)
        except models.Shipping_Details.DoesNotExist:
            self.create(request, *args, **kwargs)
            return JsonResponse({"message": "successfully created"}, status=201)


class CreateOrder(APIView):
    def post(self, request):
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
        else:
            return JsonResponse({"error": serializer.errors}, status=400)
        
        cart = request.data.get('cart', [])
        savedItems = []

        for item in cart:
            product_id = item.get('id')
            seller_id = item.get('seller_id')
            price = Decimal(item.get('price'))
            quantity = item.get('quantity')

            if not product_id and quantity is None:
                return JsonResponse({"error": "Missing vital details"}, status=400)
            if not models.Products.objects.filter(id=product_id).exists():
                return JsonResponse({"error": "Product Not found"}, status=404)
            
            product = models.Products.objects.get(id=product_id)
            serializer = serializers.ProductsOrderedSerializer(data={
                'order_id': order.id,
                'product_id': product_id,
                'seller_id': seller_id,
                'price': price,
                'quantity': quantity
            }) 
            if serializer.is_valid():
                orders_items = serializer.save()
                savedItems.append(orders_items)
                product.Sold = True
                product.save()
            else:
                return JsonResponse({"error": serializer.errors}, status=400)
        savedItems_data = serializers.ProductsOrderedSerializer(savedItems, many=True).data
        return JsonResponse({"message": "Order created successfully","savedItems": savedItems_data}, status=201)

class Order_Details(APIView):
    def post(self, request):
        id = request.data.get('id')
        order = models.Orders.objects.get(id=id)#serialize this!
        if not order:
            return JsonResponse({"Error": "Order not found"}, status=404)
        
        order_data = serializers.OrderSerializer(order).data
        return JsonResponse({"data": order_data}, status=200)