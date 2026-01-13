from rest_framework import serializers
from .models import Product, Order
import ast

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_items_details(self, obj):
        try:
            # Превращаем строку в список
            items_list = ast.literal_eval(obj.items)
            detailed_items = []
            
            for item in items_list:
                product = Product.objects.filter(id=item['id']).first()
                if product:
                    detailed_items.append({
                        'name': product.name,
                        'quantity': item['quantity'],
                        'price': product.price,
                        'image': product.image.url if product.image else None
                    })
            return detailed_items
        except:
            return []