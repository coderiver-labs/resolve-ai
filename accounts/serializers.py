
# DRF
from rest_framework import serializers


# import models
from accounts.models import CustomUser



# create serializer hare



# admin serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ["is_superuser", "is_staff", "is_verified", "is_active"]
        extra_kwargs = {"password": {"write_only": True},}


