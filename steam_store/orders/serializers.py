from rest_framework import serializers
from .models import Order, OrderItem, OrderPayment, OrderPaymentPostback
from store.serializers import SteamPayReplenishmentSerializer
from nicepay.models import NicePay


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        exclude = ('order',)



class OrderPaymentPostbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentPostback
        fields = '__all__'
        read_only_fields = ('created',)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        # read_only_fields = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    order_payment = OrderPaymentSerializer(read_only=True, )
    order_items = OrderItemSerializer(many=True, source='items')
    total_sum = serializers.IntegerField(source='get_total_cost', read_only=True)
    postbacks = OrderPaymentPostbackSerializer(many=True, read_only=True,)

    def create(self, validated_data):
        order_items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order_items_models = [OrderItem(order=order, **order_item) for order_item in order_items]
        OrderItem.objects.bulk_create(order_items_models)
        if NicePay.is_total_price_exceeded(amount=order.get_total_cost()):
            order.delete()
            limits = NicePay.get_limits()
            raise serializers.ValidationError(f'Incorrect amount, must be in ({limits["min"]}, {limits["max"]})')
        order.create_pay_link()
        return order

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        self._validate_order_items_exists(data)
        return data

    def _validate_order_items_exists(self, data):
        """Проверить что заказ не пустой"""
        if not data['items']:
            raise serializers.ValidationError('Empty order items')


class PublicOrderSerializer(OrderSerializer):
    postbacks = None
    class Meta():
        model = Order
        exclude = ('sendet_data',)

