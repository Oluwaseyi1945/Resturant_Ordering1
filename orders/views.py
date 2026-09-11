from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer, OrderSerializer


class MenuItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        menu_items = MenuItem.objects.filter(is_available=True)
        serializer = MenuItemSerializer(menu_items, many=True)

        return Response(serializer.data)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request):
        items = request.data.get('items')

        if not items:
            return Response(
                {'error': 'At least one menu item is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = Order.objects.create(
            customer=request.user
        )

        for item in items:
            menu_item_id = item.get('menu_item')
            quantity = item.get('quantity')

            if not menu_item_id or not quantity:
                order.delete()
                return Response(
                    {'error': 'Each item must have menu_item and quantity.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
            except MenuItem.DoesNotExist:
                order.delete()
                return Response(
                    {'error': f'Menu item {menu_item_id} does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not menu_item.is_available:
                order.delete()
                return Response(
                    {
                        'error': f'{menu_item.name} is currently unavailable.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if quantity < 1:
                order.delete()
                return Response(
                    {'error': 'Quantity must be at least 1.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(
                id=pk,
                customer=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)

        return Response(serializer.data)



class OrderAddItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(
                id=pk,
                customer=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only pending orders can be modified
        if order.status != 'pending':
            return Response(
                {'error': 'Only pending orders can be modified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        menu_item_id = request.data.get('menu_item')
        quantity = request.data.get('quantity')

        if not menu_item_id or not quantity:
            return Response(
                {'error': 'menu_item and quantity are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {'error': 'Menu item not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not menu_item.is_available:
            return Response(
                {'error': f'{menu_item.name} is currently unavailable.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity < 1:
            return Response(
                {'error': 'Quantity must be at least 1.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class OrderItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, item_id):
        try:
            order = Order.objects.get(
                id=pk,
                customer=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only pending orders can be modified
        if order.status != 'pending':
            return Response(
                {'error': 'Only pending orders can be modified.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order_item = OrderItem.objects.get(
                id=item_id,
                order=order
            )
        except OrderItem.DoesNotExist:
            return Response(
                {'error': 'Order item not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        order_item.delete()

        return Response(
            {'message': 'Item removed successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class OrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        # Only staff can change order status
        if not request.user.is_staff:
            return Response(
                {'error': 'Only staff can change order status.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {'error': 'Status is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_transitions = {
            'pending': ['preparing', 'cancelled'],
            'preparing': ['ready'],
            'ready': ['completed'],
            'completed': [],
            'cancelled': [],
        }

        allowed_statuses = valid_transitions.get(order.status, [])

        if new_status not in allowed_statuses:
            return Response(
                {
                    'error': (
                        f'Invalid status transition from '
                        f'{order.status} to {new_status}.'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        serializer = OrderSerializer(order)

        return Response(serializer.data)