from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MenuItem, Order


class RestaurantAPITests(APITestCase):

    def setUp(self):
        # Create customers
        self.customer1 = User.objects.create_user(
            username='customer1',
            password='customer123'
        )

        self.customer2 = User.objects.create_user(
            username='customer2',
            password='customer123'
        )

        # Create menu items
        self.available_item = MenuItem.objects.create(
            name='Jollof Rice',
            description='Nigerian jollof rice',
            price=4500,
            category='Main Course',
            is_available=True
        )

        self.unavailable_item = MenuItem.objects.create(
            name='Unavailable Rice',
            description='Not currently available',
            price=5000,
            category='Main Course',
            is_available=False
        )

        # Create an order belonging to customer2
        self.order = Order.objects.create(
            customer=self.customer2,
            status='pending'
        )

        # Get JWT token for customer1
        refresh = RefreshToken.for_user(self.customer1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

    def test_customer_cannot_view_another_customers_order(self):
        response = self.client.get(
            f'/api/orders/{self.order.id}/'
        )

        self.assertEqual(response.status_code, 404)

    def test_unavailable_menu_item_cannot_be_ordered(self):
        response = self.client.post(
            '/api/orders/',
            {
                'items': [
                    {
                        'menu_item': self.unavailable_item.id,
                        'quantity': 1
                    }
                ]
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_customer_cannot_change_order_status(self):
        response = self.client.patch(
            f'/api/orders/{self.order.id}/status/',
            {
                'status': 'preparing'
            },
            format='json'
        )

        self.assertEqual(response.status_code, 403)