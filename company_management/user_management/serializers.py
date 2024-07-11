import re

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import User
from role_management.models import Role
from .utils import send_custom_email


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'role', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', value):
            raise ValidationError("Password must contain at least 1 uppercase letter, 1 lowercase letter, and 1 number")
        return value


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError('No user is associated with this email address.')
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri(f'/api/reset-password-confirm/{uid}/{token}/')
        print("=========reset_link=======", reset_link)
        send_custom_email(reset_link=reset_link, recipient_list=[user.email])


class PasswordResetConfirmSerializer(serializers.Serializer):

    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError('Passwords do not match.')
        return data

    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save()


class UserUpdateSerializer(serializers.ModelSerializer):

    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
