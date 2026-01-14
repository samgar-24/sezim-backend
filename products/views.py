from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Это гарантирует, что Django ищет токен
def user_orders(request):
    # Если ты админ, убедись, что заказы в БД привязаны к пользователю 'admin'
    orders = Order.objects.filter(user=request.user).order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
# 1. РЕГИСТРАЦИЯ
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    try:
        if User.objects.filter(username=data['email']).exists():
            return Response({'error': 'Пользователь с таким email уже существует'}, status=400)
            
        user = User.objects.create_user(
            username=data['email'], 
            email=data['email'],
            password=data['password'],
            first_name=data.get('firstName', '')
        )
        return Response({'message': 'Пользователь успешно создан'}, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# 2. СПИСОК ТОВАРОВ
@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# 3. СОЗДАНИЕ ЗАКАЗА
@api_view(['POST'])
@permission_classes([AllowAny]) # Позволяем гостям тоже делать заказы
def create_order(request):
    data = request.data
    items = data.get('items', [])
    total_calculated = 0
    items_summary = ""

    try:
        for item in items:
            product = Product.objects.get(id=item['id'])
            subtotal = product.price * item['quantity']
            total_calculated += subtotal
            items_summary += f"• {product.name} (x{item['quantity']}) — {subtotal} ₸\n"
            
        user = request.user if request.user.is_authenticated else None

        order = Order.objects.create(
            user=user,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            address=f"{data.get('city')}, {data.get('street')}",
            total_price=total_calculated,
            items=str(items),
            status='pending'
        )

        # Отправка письма
        subject = f'Ваш заказ #{order.track_id} оформлен!'
        message = (
            f"Здравствуйте, {order.first_name}!\n\n"
            f"НОМЕР ЗАКАЗА: {order.track_id}\n"
            f"ИТОГО К ОПЛАТЕ: {order.total_price} ₸\n\n"
            f"ВАШИ ТОВАРЫ:\n{items_summary}\n"
            f"ОТСЛЕДИТЬ: https://sezim-frontend-k3wn5xaid-samgar-24s-projects.vercel.app/track?id={order.track_id}"
        )

        send_mail(subject, message, 'raceawm@gmail.com', [order.email], fail_silently=False)

        return Response({
            'message': 'Заказ создан!', 
            'track_id': order.track_id 
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# 4. ОТСЛЕЖИВАНИЕ ЗАКАЗА (Публичное)
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
@permission_classes([IsAuthenticated])
def user_orders(request):
    print(f"Запрос от пользователя: {request.user}")
    # Если ты зашел как admin, Django ищет заказы, где поле user = твой admin-user
    orders = Order.objects.filter(user=request.user).order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
# 6. АДМИНКА: Получить все заказы (только для персонала)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_orders(request):
    status_filter = request.query_params.get('status')
    orders = Order.objects.all().order_by('-id')
    if status_filter:
        orders = orders.filter(status=status_filter)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# 7. АДМИНКА: Сменить статус заказа
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        new_status = request.data.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return Response({'status': order.status})
        return Response({'error': 'Статус не указан'}, status=400)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=404)    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    return Response({
        'firstName': request.user.first_name,
        'email': request.user.email,
        'username': request.user.username,
        'is_staff': request.user.is_staff  # <--- Добавляем эту проверку
    })