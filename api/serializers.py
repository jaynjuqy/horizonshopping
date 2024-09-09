from rest_framework import serializers
from. import models

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = models.Products
        fields = '__all__' 

    def get_image_url(self, obj):
        return obj.Image.url if obj.Image else None
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['Image'] = representation.pop('image_url', None)
        return representation

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shipping_Details
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orders
        fields = '__all__'

class ProductsOrderedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Products_Ordered
        fields = '__all__'

    def create(self, validated_data):
        order_id = validated_data.pop('order_id')
        product_id = validated_data.pop('product_id')
        seller_id = validated_data.pop('seller_id')
        price = validated_data.pop('price')
        quantity = validated_data.pop('quantity')

        order_items = models.Products_Ordered.objects.create(
            order_id=order_id,
            product_id=product_id,
            seller_id=seller_id,
            price=price,
            quantity=quantity
        )
        return order_items