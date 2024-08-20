from rest_framework import generics
from . import serializers, models
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from decimal import Decimal, InvalidOperation


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
