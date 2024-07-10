from django.db import models
from django.core.validators import MinValueValidator
import requests as req
import json


class NicePay:
    MIN_ORDER_PRICE = 10
    MAX_ORDER_PRICE = 990
    PAY_URL = 'http://127.0.0.1:8000/nicepay/payment/'


class Merchants(models.Model):
    """Пользователь"""
    id = models.CharField(max_length=20, primary_key=True)
    secret = models.CharField(max_length=50, unique=True)


class Payment(models.Model):
    WAIT_PAY = 'wait_pay'
    PAYMENT_STATUSES = (
        (WAIT_PAY, WAIT_PAY),
        ('wait_approve', 'wait_approve'),
        ('approved', 'approved'),
        ('not_approved', 'not_approved')
    )
    """Заказ"""
    payment_id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey(Merchants, on_delete=models.CASCADE)
    CURRENCIES = (
        ('USD', 'UDS'),
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
        self.status = 'wait_approve'
        self.save()

    def approve(self):
        self.status = 'approved'
        self.save()
        self.send_payment_postback()

    def not_approve(self):
        self.status = 'not_approved'
        self.save()
        self.send_payment_postback()

    def send_payment_postback(self):
        if self.status not in ('approved', 'not_approved'):
            raise ValueError('Cant send post back of not complete payment')
        result = 'success' if self.status == 'approved' else 'error'
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
