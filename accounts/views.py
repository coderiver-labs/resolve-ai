from django.db import transaction

# DRF
from rest_framework.response import Response
from rest_framework import status

# import base views
from accounts.base_views import BaseUserViewSet
from utils.public_base_APIView import PublicGenericAPIView


# import serializers
from rest_framework.serializers import Serializer
from accounts.serializers import UserSerializer

# models
from accounts.models import CustomUser

# services
from accounts.services.user_service import UserCreationService

# import audit log
from audit.services import AuditService

# Create your views here.



class UserViewSet(BaseUserViewSet):
     serializer_class = UserSerializer
     queryset = CustomUser.objects.all()

     
    
     def perform_create(self, serializer: Serializer):
          user = UserCreationService.execute(
               validated_data=serializer.validated_data,
               request=self.request
          )
          serializer.instance = user

          
     def perform_update(self, serializer: Serializer):

          with transaction.atomic():
               instance = self.get_object()

               AuditService.update_log(
                    actor=self.request.user,
                    instance=instance,
                    validated_data=serializer.validated_data,
                    request=self.request,
                    description="User Update"
               )
               serializer.save() # updated_instance

               
     def perform_destroy(self, instance: CustomUser):
          with transaction.atomic():

               AuditService.delete_log(
                    actor=self.request.user,
                    instance=instance,
                    request=self.request,
                    description="user Delete with user_profile, user_contact and all user info"
               )
               instance.delete()
          