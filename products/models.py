from django.db import models
from django.conf import settings
import datetime

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    description = models.TextField(blank=True)
    sizes = models.CharField(max_length=100, default="S, M, L, XL")

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('processing', 'В обработке'),
        ('shipped', 'В пути'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    track_id = models.CharField(max_length=50, unique=True, editable=False, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    # Разделяем адрес на поля, как во фронтенде
    city = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    apartment = models.CharField(max_length=50, null=True, blank=True)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.track_id:
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            count = Order.objects.filter(created_at__date=datetime.date.today()).count() + 1
            self.track_id = f"{date_str}-{count:03d}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items_rel', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, null=True, blank=True)