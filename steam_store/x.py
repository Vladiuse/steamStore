import requests as req
from pprint import pprint

class A:

    def get(self):
        res = req.get('https://google.com')
        return res

def create_order():
    data = {
        'email': 'some@some.email',
        'phone_number': '123123123123',
        'order_items': [
            {'product': '777-usd', 'quantity': 1},
            # {'product': '20-usd', 'quantity': 5},
        ]
        # 'order_items': 1,
    }

    res = req.post('http://127.0.0.1:8000/orders/orders/', json=data)
    print(res.status_code)
    print(res.json())


#


def create_payment():
    data = {
        'merchant_id': 'vlad',
        'secret': 'vlad2030',
        'order_id': '123',
        'customer': 'vladiuse@gmailc.com',
        'amount': 10,
        'currency': 'USD',
        'method': 'post',
    }
    res = req.post('http://127.0.0.1:8000/nicepay/payment/', json=data)
    print(res.status_code)
    pprint(res.json())


def send_postback():
    data = {
        'order_id': 'bd5c6be7-bf70-42c9-aee8-5fb4d7f54701',
        'payment_id': '123',
        'merchant_id': '123',
        'amount': '100',
        'amount_currency': 'USD',
        'profit': '123',
        'profit_currency': 'USDT',
        'method': 'post',
        'hash':'123',
        'result': 'success',
    }
    res = req.post('http://127.0.0.1:8000/orders/orders/postback/', json=data)
    print(res.status_code)
    print(res.json())


create_order()
