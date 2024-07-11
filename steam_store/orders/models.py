from django.db import models
from store.models import SteamPayReplenishment
from uuid import uuid4
from requests.exceptions import RequestException, HTTPError
import requests as req
from nicepay.models import NicePay
from django.core.validators import MinValueValidator


class Order(models.Model):
    """Модель заказа"""
    NOT_PAYED = 'not_payed'
    PAYED = 'payed'
    ERROR_PAY = 'pay_error'
    STATUSES = (
        (NOT_PAYED, NOT_PAYED),
        (PAYED, PAYED),
        (ERROR_PAY, ERROR_PAY),
    )

    order_id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(max_length=34)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default=NOT_PAYED)
    created = models.DateTimeField(auto_now_add=True)
    error_payment_request = models.JSONField(blank=True, default=None)

    def get_total_cost(self) -> int:
        """Получить полную стоимость заказа"""
        return sum(item.get_cost() for item in self.items.all())

    @property
    def customer_info(self):
        info = f'{self.email}:{self.phone_number}'
        if len(info) > 50:
            info = self.email
        return info

    def create_pay_link(self) -> None:
        """Создать платежную ссылку в nicepay"""
        error_data = None
        data = {
            'merchant_id': NicePay.MERCHANT_ID,
            'secret': NicePay.SECRETS,
            'order_id': str(self.order_id),
            'customer': self.customer_info,
            'amount': self.get_total_cost(),
            'method': 'post',
            'currency': NicePay.CURRENCY,
        }
        try:
            res = req.post(NicePay.PAY_URL, json=data)
            res.raise_for_status()
            res_data = res.json()
            if res_data['status'] == 'success':
                OrderPayment.objects.create(order=self, **res_data['data'])
            else:
                error_data = res_data
        except HTTPError as error:
            error_data = {
                'status': 'error',
                'error_type': type(error),
                'error_text': 'status code not 200',
                'status_code': res.status_code,
                'data': str(res.text),
            }
        except RequestException as error:
            error_data = {
                'status': 'error',
                'error_type': type(error),
                'error_text': str(error),
            }
        if error_data:
            self.payment_request = error_data
            self.save()

    def set_payment_status(self, status: str) -> None:
        """Изменить статус платежа заказа"""
        if status not in (Order.PAYED, Order.ERROR_PAY):
            raise ValueError('Incorrect Order status ')
        self.status = status
        self.save()


class OrderItem(models.Model):
    """Товары заказа и из количество"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(SteamPayReplenishment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,
                                           validators=[MinValueValidator(1), ],
                                           )

    def get_cost(self) -> int:
        """Получить стоимоть товарной позиции"""
        return self.product.amount * self.quantity


class OrderPayment(models.Model):
    """Обьект платежа и информации о нем"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order_payment')
    payment_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    link = models.URLField()
    expired = models.CharField(max_length=100)


class OrderPaymentPostback(models.Model):
    """Постбэк от платежной системы о статусе платежа"""
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

    def save(self, **kwargs) -> None:
        super().save(**kwargs)
        # При сохранении изменить статус заказа в зависимости от полученого статуса от nicepay
        if self.result == 'success':
            self.order_id.set_payment_status(Order.PAYED)
        elif self.result == 'error':
            self.order_id.set_payment_status(Order.ERROR_PAY)
