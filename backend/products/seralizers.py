from rest_framework import serializers

from .models import Category, Product, PromotionEvent


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "required": "Product name is required",
                    "blank": "Product name cannot be empty",
                    "max_length": "Product name is too long (max 255 characters)",
                }
            },
            "price": {
                "error_messages": {
                    "required": "Price is required",
                    "invalid": "Price must be a valid number",
                    "max_digits": "Price has too many digits",
                }
            },
            "stock": {
                "error_messages": {
                    "required": "Stock quantity is required",
                    "invalid": "Stock must be a valid number",
                }
            },
        }

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price Must be greater than zero")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("stock cannot be negative")
        return value


class PromotionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionEvent
        fields = ["id", "name", "price_reduction", "start_date ", "end_date"]
        read_only_fields = (
            [
                "id",
            ],
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "level", "parent"]
        read_only_fields = [
            "id",
        ]
