from django.contrib.auth.models import User
from django.core.mail import send_mail, get_connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    data = request.data
    cart_items = data.get('items', [])
    
    try:
        # 1. Создаем основной заказ
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            city=data.get('city'),
            street=data.get('street'),
            apartment=data.get('apartment'),
            total_price=0
        )

        total = 0
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            qty = int(item['quantity'])
            price = float(item['price'])
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=price,
                size=item.get('size')
            )
            total += price * qty

        order.total_price = total
        order.save()

        # 2. Почта с жестким таймаутом (чтобы не вешать сервер)
        try:
            connection = get_connection(timeout=3)
            send_mail(
                f"Заказ №{order.track_id} — SEZIM",
                f"Спасибо за заказ!\nТрек: {order.track_id}\nСумма: {total} ₸",
                'raceawm@gmail.com',
                [order.email],
                fail_silently=True,
                connection=connection
            )
        except Exception as e:
            logger.error(f"Mail delivery failed: {e}")

        # ОБЯЗАТЕЛЬНО ВОЗВРАЩАЕМ ОТВЕТ
        return Response({"track_id": order.track_id}, status=201)

    except Exception as e:
        logger.error(f"ORDER ERROR: {str(e)}")
        return Response({"error": str(e)}, status=400)
# 5. УПРАВЛЕНИЕ СТАТУСОМ (Для админа)
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        status_value = request.data.get('status')
        if status_value:
            order.status = status_value
            order.save()
            return Response({'message': 'Статус обновлен'})
        return Response({'error': 'Статус не указан'}, status=400)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=404)
@api_view(['GET'])
@permission_classes([AllowAny])
def track_order(request, track_id):
    try:
        order = Order.objects.get(track_id=track_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    try:
        if User.objects.filter(username=data['email']).exists():
            return Response({'error': 'Email уже занят'}, status=400)
        user = User.objects.create_user(
            username=data['email'], email=data['email'],
            password=data['password'], first_name=data.get('firstName', '')
        )
        return Response({'message': 'Created'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    return Response({
        'firstName': request.user.first_name,
        'email': request.user.email,
        'is_staff': request.user.is_staff
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)