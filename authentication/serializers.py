from django.contrib.auth.hashers import check_password

# DRF
from rest_framework import serializers
from rest_framework.authentication import authenticate


# models
from accounts.models import CustomUser


# Create Serializers



# login api serializer
class LoginUserSerializer(serializers.Serializer):
    """
    Simple login serializer — email normalized here as well.
    """

    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid email or password"})
        attrs["user"] = user
        return attrs




def get_user_basic_info(*, user: CustomUser) -> dict:
    return {
        "uuid": user.uuid,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }




class DummySerializer(serializers.Serializer):
    pass

# dummy for swagger
class ProfileSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(allow_null=True)
    position = serializers.CharField(required=False)


# dummy for swagger
class GetAccessTokenResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


# login api serializer
class LoginUserSerializer(serializers.Serializer):
    """
    Simple login serializer — email normalized here as well.
    """

    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid email or password"})
        attrs["user"] = user
        return attrs



# resend verify email serializer
class ResendVerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        # user = CustomUser.objects.get(email=email)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"user": "user does't exist"})
        
        attrs["user"] = user
        return attrs



# reset password serializer
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=7, max_length=15)

    def validate(self, attrs):
        from authentication.services.validations import check_prevues_password

        user = self.context.get("user")
        password = attrs.get("password")
        check_prevues_password(old_password=user.password, new_password=password)
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=7, max_length=15)
    new_password = serializers.CharField(min_length=7, max_length=15)

    def validate(self, attrs):
        from authentication.services.validations import check_prevues_password


        user = self.context.get("user")
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")

        if not check_password(old_password, user.password):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect."}
            )
        check_prevues_password(old_password=user.password, new_password=new_password)
        return attrs
