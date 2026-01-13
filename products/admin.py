from django.contrib import admin
from .models import Product, Order # Добавь Order

admin.site.register(Product)
admin.site.register(Order) # Теперь заказы появятся в админке