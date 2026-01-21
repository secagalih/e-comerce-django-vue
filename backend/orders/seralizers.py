from products.seralizers import ProductSerializer
from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSeralizer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity"]
        read_only_fields = ["id"]


class OrderDetailSerializer(serializers.ModelSerializer):
    order_item = OrderItemSeralizer(source="orderitem_set", many=True, read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "user",
            "user_email",
            "order_items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class OrderListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing orders"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "user_email",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
