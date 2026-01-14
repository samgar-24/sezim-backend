from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from products import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls), 
    
    # Авторизация
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.register_user),
    path('api/me/', views.get_user_profile), 
    
    # Продукты
    path('api/products/', views.product_list),
    
    # Заказы и трекинг
    path('api/orders/', views.create_order),
    path('api/my-orders/', views.user_orders),
    path('api/track/<str:track_id>/', views.track_order),
    
    # Админ-панель (управление заказами)
    path('api/orders-list/', views.get_orders),
    path('api/orders/<int:pk>/status/', views.update_order_status),
]

# ВАЖНО: Добавляем раздачу медиа-файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # На продакшене (Railway) Django тоже должен уметь отдавать файлы, если нет внешнего хранилища
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)