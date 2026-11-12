
# DRF
from rest_framework import serializers


# import models
from accounts.models import CustomUser



# create serializer hare



# admin serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]
        read_only_fields = ["is_superuser", "is_staff", "is_verified", "is_active"]

