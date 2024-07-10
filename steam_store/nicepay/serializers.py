from rest_framework import serializers
from .models import Merchants, Payment
from decimal import Decimal


class PayMentSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='payment-detail')
    pay_link = serializers.HyperlinkedIdentityField(view_name='payment-pay', read_only=True)
    approved = serializers.HyperlinkedIdentityField(view_name='payment-approve', read_only=True)
    not_approved = serializers.HyperlinkedIdentityField(view_name='payment-not-approve', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if instance.status == 'wait_pay':
            repr.pop('approved')
            repr.pop('not_approved')
        if instance.status == 'wait_approve':
            repr.pop('pay_link')
        elif instance.status in ('approved', 'not_approved'):
            repr.pop('approved')
            repr.pop('not_approved')
            repr.pop('pay_link')
        return repr



class PayMentCreateSerializer(serializers.ModelSerializer):
    merchant_id = serializers.CharField()
    secret = serializers.CharField()


    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('merchant',)

    def create(self, validated_date):
        merchant_id = validated_date.pop('merchant_id')
        secret = validated_date.pop('secret')
        merchant = Merchants.objects.get(id=merchant_id, secret=secret)
        payment = Payment.objects.create(merchant=merchant,
                                         **validated_date,
                                         )
        return payment

    def validate(self, data):
        self._check_merchant_exist(data)
        return data

    def _check_merchant_exist(self, data):
        merchant_id = data['merchant_id']
        secret = data['secret']
        try:
            Merchants.objects.get(id=merchant_id, secret=secret)
        except Merchants.DoesNotExist:
            raise serializers.ValidationError('Merchant not found')

class PaymentLinkSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='payment-detail')
    class Meta:
        model = Payment
        fields = ('payment_id', 'amount', 'currency', 'link', 'expired')

