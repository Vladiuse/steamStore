from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from .serializers import OrderSerializer, OrderPaymentPostbackSerializer
from .models import Order
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import action


@api_view()
def orders_root(request, format=None):
    return Response({
        reverse('order-list', request=request, format=format)
    })
class OrderView(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    @action(detail=False, methods=['post'])
    def postback(self, request):
        serializer = OrderPaymentPostbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'status': 'success',
        })



