from django.test import TestCase
from unittest.mock import patch, Mock
from orders import models
from store.models import SteamPayReplenishment
from nicepay.models import NicePay

Order = models.Order
OrderItem = models.OrderItem

class OrderCreatePayLinkTest(TestCase):
    CORRECT_RESPONCE = {
        "status": "success",
        "data": {
            "payment_id": "bVz657-bd8755-040148-6c9b6c-e47dld",
            "amount": 12350,
            "currency": "USD",
            "link": "https://nicepay.io/pay/657b458302a2e415c90bce69",
            "expired": "1702577504"
        }
    }

    def setUp(self):
        self.product_1 = SteamPayReplenishment.objects.create(replenishment=10, amount=10)
        self.product_2 = SteamPayReplenishment.objects.create(replenishment=20, amount=20)

    def test_get_payment_link_data(self):
        order = Order.objects.create(email='some@some.com', phone_number='+1234567890')
        OrderItem.objects.create(
            order=order,
            product=self.product_1,
            quantity=1,
        )
        data = order.get_data_for_payment_link()
        self.assertEqual(data['customer'], 'some@some.com:+1234567890')
        self.assertEqual(data['amount'], 10 * 100)
        self.assertEqual(data['currency'], NicePay.CURRENCY)


    # @patch('models.req.post')
    # def test_responce_correct(self, mock_post):
    #     order = Order.objects.create(email='some@some.com', phone_number='+1234567890')
    #     order_item_1 = OrderItem.objects.create(
    #         order=self.order,
    #         product=self.product_1,
    #         quantity=1,
    #     )
    #     mock_response = Mock()
    #     mock_response.return_value = '123'
