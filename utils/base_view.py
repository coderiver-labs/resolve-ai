from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet

class PublicViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    A viewset that provides default `list()` and `retrieve()` actions.
    """
    pass

class BaseModelViewSet(ModelViewSet):
    throttle_scope = "api"
    lookup_field = "uuid"

class BaseGenericApiView(GenericAPIView):
    throttle_scope = "api"
    lookup_field = "uuid"

