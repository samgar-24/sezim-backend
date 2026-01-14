from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_image = serializers.ReadOnlyField(source='product.image')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price', 'size']

class OrderSerializer(serializers.ModelSerializer):
    # Поле items должно совпадать с тем, что ожидает фронтенд
    items = OrderItemSerializer(source='items_rel', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'track_id', 'first_name', 'last_name', 'email', 
            'city', 'street', 'apartment', 'total_price', 
            'status', 'created_at', 'items'
        ]