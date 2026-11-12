# DRF
from rest_framework.response import Response
from rest_framework import status

# import base views
from accounts.base_views import BaseUserViewSet
from utils.public_base_APIView import PublicGenericAPIView


# import serializers
from accounts.serializers import UserSerializer
# models
from accounts.models import CustomUser

# Create your views here.


class UserViewSet(BaseUserViewSet):
     serializer_class = UserSerializer
     queryset = CustomUser.objects.all()
    


