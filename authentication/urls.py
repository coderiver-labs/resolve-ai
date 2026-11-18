from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# views
from authentication import views



# Router registration

# url patterns

urlpatterns = [
    path("get-csrf-token/", views.GetCSRFToken.as_view(), name="get_csrf_token"),
    path("get-access-token/", views.GetAccessTOkenAPI.as_view(), name="get_access_token"),
    path("login/", views.LoginAPIView.as_view(), name="get_csrf_token"),
    path("logout/", views.LogoutGenericAPIView.as_view(), name="logout"),

]
