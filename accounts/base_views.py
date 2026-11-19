
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from utils.base_view import BaseModelViewSet
# model
from accounts.models import CustomUser

# serializer
from accounts.serializers import AdminUserSerializer, StaffUserSerializer

class BaseUserViewSet(BaseModelViewSet):

    def get_serializer(self, *args, **kwargs):
        user: CustomUser = self.request.user

        if user.role == "admin" or user.is_superuser:
            return AdminUserSerializer

        if user.role == "staff":
            return StaffUserSerializer
        
        
    ...