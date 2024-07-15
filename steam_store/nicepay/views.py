from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from .serializers import PayMentSerializer, PayMentCreateSerializer, PaymentLinkSerializer
from .models import Payment, NicePay
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated


@api_view()
@permission_classes([IsAuthenticated,])
def nicepay_root(request, format=None):
    return Response({
        'payments': reverse(viewname='payment-list', request=request, format=format),
        'nicepay_vars': reverse(viewname='nicepay_vars', request=request, format=format),
    })

@api_view()
@permission_classes([IsAuthenticated,])
def nicepay_vars(request, format=None):
    data = {
        'CURRENCY': NicePay.CURRENCY,
        'PAY_URL': NicePay.PAY_URL,
        'MERCHANT_ID': NicePay.MERCHANT_ID,
        'SECRETS': NicePay.SECRETS,

    }
    return Response(data)


class PaymentView(ModelViewSet):
    queryset = Payment.objects.all()


    def get_serializer_class(self):
        if self.action == 'create':
            return PayMentCreateSerializer
        else:
            return PayMentSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAuthenticated(), ]
        else:
            self.permission_classes = []
        return self.permission_classes


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




