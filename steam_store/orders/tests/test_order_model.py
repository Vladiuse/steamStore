from orders.models import Order, OrderItem
from django.test import TestCase
from store.models import SteamPayReplenishment
from django.core.exceptions import ValidationError


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.product_1 = SteamPayReplenishment.objects.create(replenishment=10, amount=10)
        self.product_2 = SteamPayReplenishment.objects.create(replenishment=20, amount=20)
        self.order = Order.objects.create(email='some@some.com', phone_number='123123123')

        self.assertEqual(SteamPayReplenishment.objects.count(), 2)
        self.assertEqual(Order.objects.count(), 1)

    def test_order_item_price_1(self):
        order_item_1 = OrderItem.objects.create(
            order=self.order,
            product=self.product_1,
            quantity=1,
        )
        self.assertEqual(order_item_1.get_cost(), 10)

    def test_order_item_price_2(self):
        order_item_1 = OrderItem.objects.create(
            order=self.order,
            product=self.product_2,
            quantity=2,
        )
        self.assertEqual(order_item_1.get_cost(), 40)

    def test_order_item_quantity_incorrect(self):
        values = (-1, 0)
        for quantity in values:
            with self.subTest(quantity=quantity):
                order_item_1 = OrderItem(
                    order=self.order,
                    product=self.product_2,
                    quantity=quantity,
                )
                with self.assertRaises(ValidationError):
                    order_item_1.full_clean()


class OrderTest(TestCase):

    def setUp(self):
        self.product_1 = SteamPayReplenishment.objects.create(replenishment=10, amount=10)
        self.product_2 = SteamPayReplenishment.objects.create(replenishment=20, amount=20)

    def test_order_price_one_item(self):
        order = Order.objects.create(email='some@some.com', phone_number='123123123')
        OrderItem.objects.create(
            order=order,
            product=self.product_1,
            quantity=1,
        )
        self.assertEqual(order.get_total_cost(), 1 * 10)

    def test_order_cost_few_items(self):
        order = Order.objects.create(email='some@some.com', phone_number='123123123')
        OrderItem.objects.create(
            order=order,
            product=self.product_1,
            quantity=1,
        )
        OrderItem.objects.create(
            order=order,
            product=self.product_2,
            quantity=2,
        )
        self.assertEqual(order.get_total_cost(), 1 * 10 + 2 * 20)

    def test_set_status_incorrect_status(self):
        order = Order.objects.create(email='some@some.com', phone_number='123123123')
        with self.assertRaises(ValueError):
            order.set_payment_status(status='123')

        with self.assertRaises(ValueError):
            order.set_payment_status(status=Order.NOT_PAYED)

    def test_set_status_error_payed(self):
        order = Order.objects.create(email='some@some.com', phone_number='123123123')
        order.set_payment_status(status=Order.ERROR_PAY)
        self.assertEqual(order.status, Order.ERROR_PAY)

    def test_set_status_payed(self):
        order = Order.objects.create(email='some@some.com', phone_number='123123123')
        order.set_payment_status(status=Order.PAYED)
        self.assertEqual(order.status, Order.PAYED)
