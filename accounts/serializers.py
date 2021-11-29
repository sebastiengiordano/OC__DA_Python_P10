from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password])
    password_check = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_check",
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
            'password_check': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_check']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        # user.set_password(validated_data['password'])
        # user.save()

        return user
