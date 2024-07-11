from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view()
def api_root(request, format=None):
    return Response({
        'orders_app': reverse('orders_root', request=request,format=format),
        'nice_pay_app': reverse('nicepay_root', request=request,format=format),
        'store_app': reverse('store_root', request=request,format=format),
    })