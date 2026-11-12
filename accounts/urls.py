from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# import views
from accounts import views



# Router registration
router.register("users", views.UserViewSet, basename="user_viewset")
# url patterns

urlpatterns = [
    path("", include(router.urls))
    
]
