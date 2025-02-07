from django.test import TestCase
from django.urls import reverse
from .models import Order

class OrderModelTest(TestCase):

    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Блюдо 1', 'price': 100}],
            total_price=100,
            status='pending'
        )

    def test_order_creation(self):
        self.assertEqual(self.order.table_number, 1)
        self.assertEqual(self.order.items, [{'name': 'Блюдо 1', 'price': 100}])
        self.assertEqual(self.order.total_price, 100)
        self.assertEqual(self.order.status, 'pending')

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} - Table {self.order.table_number}")

class OrderViewTest(TestCase):

    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
            items=[{'name': 'Блюдо 1', 'price': 100}],
            total_price=100,
            status='pending'
        )

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Список заказов')
        self.assertContains(response, self.order.table_number)

    def test_order_create_view(self):
        response = self.client.post(reverse('order_create'), {
            'table_number': 2,
            'item_name': ['Блюдо 2'],
            'item_price': [200]
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_update_view(self):
        response = self.client.post(reverse('order_update', args=[self.order.id]), {
            'table_number': 1,
            'item_name': ['Блюдо 1', 'Блюдо 2'],
            'item_price': [100, 200],
            'status': 'ready'
        })
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')
        self.assertEqual(len(self.order.items), 2)

    def test_order_delete_view(self):
        response = self.client.post(reverse('order_delete', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)