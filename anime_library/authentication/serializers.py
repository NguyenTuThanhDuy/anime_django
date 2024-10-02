from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.models import UserAccountInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        read_only_fields = ('is_superuser', 'is_staff', 'is_active',
                            )  # Make created_at and updated_at read-only

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)  # Remove password from serialized data
        return representation

    # Ensure `id` is not required for creation but is required for updating
    def validate(self, attrs):
        if self.instance is None and 'id' in attrs:
            raise serializers.ValidationError({"id": "ID should not be provided when creating a new user."})
        if not attrs['password'] or len(attrs['password']) < 8:
            raise serializers.ValidationError(
                {"password": "Password cannot be empty and must be more than 8 characters."})
        return super().validate(attrs)

    # Hash the password before saving
    def create(self, validated_data):
        # Remove id from validated_data to avoid any conflicts
        validated_data.pop('id', None)
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # ID is required for updating, so we don't need to remove it from validated_data
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)


class UserAccountInfoSerializer(serializers.ModelSerializer):
    user_account = UserSerializer()

    class Meta:
        model = UserAccountInfo
        fields = ['user_account', 'date_of_birth', 'phone_number']

    # Overriding create method to create UserAccount and UserAccountInfo at the same time
    def create(self, validated_data):
        user_data = validated_data.pop('user_account')

        # Use UserAccountSerializer to create and hash the password
        user_account_serializer = UserSerializer(data=user_data)
        user_account_serializer.is_valid(raise_exception=True)
        user_account = user_account_serializer.save()  # This ensures the password is hashed

        # Create the UserAccountInfo
        user_info = UserAccountInfo.objects.create(user_account=user_account, **validated_data)
        return user_info

    def update(self, instance, validated_data):
        # ID is required for updating, so we don't need to remove it from validated_data
        return super(UserAccountInfoSerializer, self).update(instance, validated_data)


class ErrorSerializer(serializers.Serializer):
    msg = serializers.CharField()
    errors = serializers.DictField(child=serializers.CharField(), required=False)
