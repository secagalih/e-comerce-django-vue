from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if self.instance:
            if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at Least 8 Character")
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)
