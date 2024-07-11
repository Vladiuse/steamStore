from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import PayMentSerializer, PayMentCreateSerializer, PaymentLinkSerializer
from .models import Payment
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.reverse import reverse


@api_view()
def nicepay_root(request, format=None):
    return Response({
        'payments': reverse(viewname='payment-list', request=request, format=format),
    })
class PaymentView(ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PayMentCreateSerializer
        else:
            return PayMentSerializer


    def create(self, request, *args, **kwargs):
        serializer = PayMentCreateSerializer(data=request.data)
        print('CREATE')
        if serializer.is_valid():
            print('IS VALID')
            payment = serializer.save()
            serializer = PaymentLinkSerializer(instance=payment, context={'request': request})
            data = {
                'status': 'success',
                'data': serializer.data,
            }
            return Response(data)
        else:
            print('ELSE')
            data = {
                'status': 'error',
                'data': serializer.errors,
            }
            return Response(data, status=400)

    @action(detail=True,methods=['get',])
    def pay(self, request, pk=None):
        payment = self.get_object()
        print(payment, type(payment))
        payment.pay()
        serializer = PayMentSerializer(instance=payment, context={'request': request})
        return Response(serializer.data)

    @action(detail=True,methods=['get',])
    def approve(self, request, pk=None):
        payment = self.get_object()
        print(payment, type(payment))
        payment.approve()
        serializer = PayMentSerializer(instance=payment, context={'request': request})
        return Response(serializer.data)

    @action(detail=True,methods=['get',])
    def not_approve(self, request, pk=None):
        payment = self.get_object()
        print(payment, type(payment))
        payment.not_approve()
        serializer = PayMentSerializer(instance=payment, context={'request': request})
        return Response(serializer.data)




