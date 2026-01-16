from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirmation', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }
  
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate_email(self, value):
        # Check if this is an update operation
        if self.instance:
            # During update, exclude current user from uniqueness check
            if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            # During create, check if email exists
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirmation before creating user
        validated_data.pop('password_confirmation', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        # Remove password_confirmation if present
        validated_data.pop('password_confirmation', None)
        
        # Update email if provided
        instance.email = validated_data.get('email', instance.email)
        
        # Update password only if provided and use set_password to hash it
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        instance.save()
        return instance