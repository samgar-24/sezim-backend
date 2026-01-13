from django.db import models
from django.conf import settings
import datetime

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.URLField(verbose_name="Ссылка на картинку")
    description = models.TextField(blank=True, verbose_name="Описание")
    sizes = models.CharField(max_length=100, default="S, M, L, XL", verbose_name="Доступные размеры")

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
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders',
        null=True, 
        blank=True
    )
    # Наш уникальный номер: ГГГГММДД-001
    track_id = models.CharField(max_length=50, unique=True, editable=False, null=True, verbose_name="Номер отслеживания")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.TextField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.track_id:
            # 1. Получаем дату
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            # 2. Считаем заказы только за СЕГОДНЯ
            today = datetime.date.today()
            count = Order.objects.filter(created_at__date=today).count() + 1
            # 3. Формируем номер
            self.track_id = f"{date_str}-{count:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.track_id} - {self.first_name}"