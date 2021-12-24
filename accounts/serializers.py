from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import update_session_auth_hash

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    '''Serialiser of custom user.'''

    password = serializers.CharField(write_only=True)
    password_check = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_check"
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()

        password = validated_data.get('password', None)
        password_check = validated_data.get('password_check', None)

        if password and password_check and password == password_check:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance


class CustomUserListSerializer(CustomUserSerializer):
    '''List serialiser of custom user.'''

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email"
        ]
