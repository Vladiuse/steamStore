from orders.models import Order
from nicepay.models import Payment

Order.objects.all().delete()
Payment.objects.all().delete()