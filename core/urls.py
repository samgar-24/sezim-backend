from django.contrib import admin
from django.urls import path
# Импортируем views из приложения products, а не из core
from products import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/products/', views.product_list),
    path('api/register/', views.register_user),
    path('api/orders/', views.create_order),
    path('api/my-orders/', views.user_orders),
    
    # ЭТОТ ПУТЬ НУЖЕН ДЛЯ ИМЕНИ И ПОЧТЫ В ПРОФИЛЕ
    path('api/me/', views.get_user_profile), 
    
    path('api/orders-list/', views.get_orders),
    path('api/orders/<int:pk>/status/', views.update_order_status),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/track/<str:track_id>/', views.track_order),
]