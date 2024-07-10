from django.db import models
import requests as req


USD = 'USD'
RUB = 'RUB'


class NicePay:
    CURRENCY = USD
    LIMITS = {
        USD: {'min': 10, 'max': 990},
        RUB: {'min': 200, 'max': 85000},
    }
    MIN_ORDER_PRICE = 10
    MAX_ORDER_PRICE = 990
    PAY_URL = 'http://127.0.0.1:8000/nicepay/payment/'
    MERCHANT_ID = 'vlad'
    SECRETS = 'vlad2030'


class Merchants(models.Model):
    """Пользователь в платежной системе"""
    id = models.CharField(max_length=20, primary_key=True)
    secret = models.CharField(max_length=50, unique=True)
    # TODO
    # добавить ссылку на постюэк о статусе платежа


class Payment(models.Model):
    """Обьект платежа"""
    WAIT_PAY = 'wait_pay'
    WAIT_APPROVE = 'wait_approve'
    APPROVED = 'approved'
    DECLINED = 'declined'

    PAYMENT_STATUSES = (
        (WAIT_PAY, WAIT_PAY),
        (WAIT_APPROVE, WAIT_APPROVE),
        (APPROVED, APPROVED),
        (DECLINED, DECLINED)
    )
    payment_id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey(Merchants, on_delete=models.CASCADE)
    CURRENCIES = (
        (USD, USD,),
        (RUB, RUB,),
    )
    order_id = models.CharField(max_length=50)
    customer = models.CharField(max_length=50)
    amount = models.DecimalField(
        max_digits=7, decimal_places=2,
    )
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    description = models.TextField(blank=True)
    method = models.CharField(max_length=50)
    success_url = models.URLField(blank=True)
    fail_url = models.URLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default=WAIT_PAY)
    expired = models.CharField(max_length=20, blank=True)

    def pay(self):
        """Пометить платеж как оплаченый и ожидающий подтверждения"""
        self.status = Payment.WAIT_APPROVE
        self.save()

    def approve(self):
        """Пометить платеж как подтвержденный"""
        self.status = Payment.APPROVED
        self.save()
        self.send_payment_postback()

    def not_approve(self):
        """Пометить платеж как откланенный"""
        self.status = Payment.DECLINED
        self.save()
        self.send_payment_postback()

    def send_payment_postback(self):
        """Отплавить постбэк пользователю о изменении статуса заказа"""
        if self.status not in (Payment.APPROVED, Payment.DECLINED):
            raise ValueError('Cant send post back of not complete payment')
        result = 'success' if self.status == Payment.APPROVED else 'error'
        data = {
            'order_id': self.order_id,
            'payment_id': self.payment_id,
            'merchant_id': self.merchant.pk,
            'amount': str(self.amount),
            'amount_currency': self.currency,
            'profit': '123',
            'profit_currency': 'USDT',
            'method': self.method,
            'hash': '123',
            'result': result,

        }
        res = req.post('http://127.0.0.1:8000/orders/orders/postback/', json=data)
        print(res.status_code)
        print(res.json())
