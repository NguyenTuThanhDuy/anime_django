from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.models import UserAccountInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'is_superuser', 'is_staff', 'is_active')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)  # Remove password from serialized data
        return representation


class UserAccountInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    # Add a nested UserSerializer to include fields in the response
    user_account = UserSerializer(read_only=True)

    class Meta:
        model = UserAccountInfo
        fields = ['user_account', 'username', 'password', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'email']

    def to_representation(self, instance):
        # Call the parent representation
        representation = super().to_representation(instance)
        # Flatten the nested user_account fields into the root of the JSON response
        user_account_data = representation.pop("user_account")
        representation.update(user_account_data)
        return representation

    def create(self, validated_data):
        # Extract user-related data and remove them from validated_data
        user_data = {
            "username": validated_data.pop("username"),
            "password": make_password(validated_data.pop("password")),
            "first_name": validated_data.pop("first_name"),
            "last_name": validated_data.pop("last_name"),
            "email": validated_data.pop("email"),
        }

        # Create the User instance
        user_account = User.objects.create(**user_data)

        # Create UserAccountInfo with the user_account relationship
        user_info = UserAccountInfo.objects.create(user_account=user_account, **validated_data)
        return user_info

    def update(self, instance, validated_data):
        # Update the related User fields
        user = instance.user_account
        user.username = validated_data.get("username", user.username)
        if "password" in validated_data:
            user.password = make_password(validated_data["password"])
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.save()

        # Update UserAccountInfo fields
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.save()

        return instance


class ErrorSerializer(serializers.Serializer):
    msg = serializers.CharField()
    errors = serializers.DictField(child=serializers.CharField(), required=False)
