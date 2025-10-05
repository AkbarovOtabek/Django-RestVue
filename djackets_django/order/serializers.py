from rest_framework import serializers
from .models import *

class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = orderItem
    fields = ('id', 'product', 'price', 'quantity')




class OrderSerializer(serializers.ModelSerializer):
  items = OrderItemSerializer(many=True)
  user = serializers.HiddenField(default=serializers.CurrentUserDefault())
  class Meta:
    model = order
    fields = (
      'id',
      'user',
      'last_name',
      'first_name',
      'email',
      'address',
      'zipcode',
      'place',
      'phone',
      'created_at',
      'paid_amount',
      'stripe_token',
      'items'
    )
  def create(self, validated_data):
    items_data = validated_data.pop('items')
    orde1 = order.objects.create(**validated_data)

    for item_data in items_data:
      orderItem.objects.create(order=orde1, **item_data)
    return orde1

