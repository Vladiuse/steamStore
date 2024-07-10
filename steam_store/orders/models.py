from django.db import models
from store.models import SteamPayReplenishment
from django.core.validators import MaxValueValidator
from nicepay.models import NicePay
from uuid import uuid4
from requests.exceptions import RequestException, HTTPError
import requests as req
from nicepay.models import NicePay


class Order(models.Model):
    NOT_PAYED = 'not_payed'
    PAYED = 'payed'
    ERROR_PAY = 'pay_error'
    STATUSES = (
        (NOT_PAYED,NOT_PAYED),
        (PAYED,PAYED),
        (ERROR_PAY,ERROR_PAY),
    )


    order_id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default=NOT_PAYED)
    created = models.DateTimeField(auto_now_add=True)

    # payment_id = models.CharField(max_length=100, blank=True)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def is_total_price_exceeded(self) -> bool:
        total_cost = self.get_total_cost()
        return NicePay.MIN_ORDER_PRICE < total_cost < NicePay.MAX_ORDER_PRICE

    def create_pay_link(self):

        data = {
            'merchant_id': 'vlad',
            'secret': 'vlad2030',
            'order_id': str(self.order_id),
            'customer': self.email,
            'amount': self.get_total_cost(),
            'method': 'post',
            'currency': 'USD',
        }
        print(data)
        try:
            res = req.post(NicePay.PAY_URL, json=data)
            res.raise_for_status()
            res_data = res.json()
            if res_data['status'] == 'success':
                order_payment = OrderPayment.objects.create(order=self,**res_data['data'])
                return order_payment
            else:
                return res_data
        except HTTPError as error:
            print(res)
            return res_data
        except RequestException as error:
            return {
                'status': 'error',
                'data': f'RequestException {error}'
            }

    def set_payment_status(self, status):
        if status not in (Order.PAYED, Order.ERROR_PAY):
            raise ValueError('Incorrect Order status')
        self.status = status
        self.save()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(SteamPayReplenishment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,
                                           # validators=[MaxValueValidator(10),],
                                           )

    def get_cost(self):
        return self.product.amount * self.quantity


class OrderPayment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_payment')
    payment_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    link = models.URLField()
    expired = models.CharField(max_length=100)


class OrderPaymentPostback(models.Model):
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='postbacks')
    result = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    merchant_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    amount_currency = models.CharField(max_length=100)
    profit = models.CharField(max_length=100)
    profit_currency = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.result == 'success':
            self.order_id.set_payment_status(Order.PAYED)
        elif self.result == 'error':
            self.order_id.set_payment_status(Order.ERROR_PAY)