# DRF
from rest_framework.response import Response
from rest_framework import status

# base views
from utils.public_base_APIView import PublicGenericAPIView
from utils.base_view import BaseGenericApiView

# serializers
from utils.serializers import DummySerializer
from authentication.serializers import (
    LoginUserSerializer,
    ResendVerifyEmailSerializer,
    ResetPasswordSerializer,
    ChangePasswordSerializer,
)


# models
from accounts.models import CustomUser

# auth
from auth.cookies import CookieHandler, AuthCookieService
from auth.validators import verify_one_time_token

# validator
from authentication.services.validations import verify_user
from authentication.services.validations import update_token_password



# custom mixin
from utils.mixins import CSRFCookieMixin

# celery 
from celery_task.task import (
    celery_verify_success_mail, 
    celery_send_reset_password_mail,
    celery_password_reset_success_mail,
    celery_send_verify_mail
)

# other
from typing import cast


# Create your views here.







"""______________________Authentication, Validation And Passwd Management________________"""


class GetCSRFToken(CSRFCookieMixin, PublicGenericAPIView):
    """
    GetCsrfToken is a public API for retrieving a CSRF token.

    - This API uses a **GET request**
    - When you call this API, a **CSRF token will be automatically set in your browser cookie**
    - The CSRF token is required for all unsafe requests such as **POST, PUT, PATCH, DELETE**
    - This improves security and prevents Cross-Site Request Forgery (CSRF) attacks
    - Rate Limit: Maximum 10 requests per minute per IP
    """

    serializer_class = DummySerializer
    
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)



class LoginAPIView(PublicGenericAPIView):
    """
    LoginGenericAPIView is a public API for user login.
    - This API uses a **POST request**
    - Required fields: `email`, `password`
    - On successful login, authentication cookies will be set in the response.
    - Rate Limit: Maximum 5 login attempts per minute per IP
    """
    # throttle_classes = [LoginThrottle]
    throttle_scope = "login"
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        response = Response({"message": "Login successfully"}, status=status.HTTP_200_OK)
        cookie = AuthCookieService(request=request, user=user)
        response = cookie.set_login_cookies(response=response)
        return response



class GetCSRFToken(CSRFCookieMixin, PublicGenericAPIView):
    """
    GetCsrfToken is a public API for retrieving a CSRF token.

    - This API uses a **GET request**
    - When you call this API, a **CSRF token will be automatically set in your browser cookie**
    - The CSRF token is required for all unsafe requests such as **POST, PUT, PATCH, DELETE**
    - This improves security and prevents Cross-Site Request Forgery (CSRF) attacks
    - Rate Limit: Maximum 10 requests per minute per IP
    """

    serializer_class = DummySerializer
    
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)



class VerifyAccountAPI(PublicGenericAPIView):
    """
    VerifyAccountAPI is a public API for verifying user accounts.
    - This API uses a **GET request**
    - The `token` parameter in the URL is a one-time token sent to the user's email for account verification.
    - On successful verification, the user's account will be marked as verified.
    """

    def get(self, request, token):
        from celery.app.task import Task

        user: CustomUser = verify_one_time_token(signed_token=token, purpose="verify_email")
        verify_user(user=user)
        task = cast(Task, celery_verify_success_mail)
        task.delay(user_uuid=str(user.uuid))
        return Response({"verify": "account verify successfully"})
    
class ResendVerificationEmailAPI(PublicGenericAPIView):
    """
    ResendVerificationEmailAPI is a public API for resending account verification emails.
    - This API uses a **POST request**
    - Required field: `email`
    - If the user is not already verified, a new verification email will be sent to the provided email address.
    - Rate Limit: Maximum 10 requests per minute per IP
    """

    serializer_class = ResendVerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        if user.is_verified:
            return Response({"message": "User has been verified"}, status=status.HTTP_200_OK)
        celery_send_verify_mail.delay(user_uuid=str(user.uuid), purpose="verify_email")
        return Response({"message": "Verify mail send successfully"}, status=status.HTTP_200_OK)


class ForgetPasswordAPI(PublicGenericAPIView):
    """
    ForgetPasswordAPI is a public API for initiating the password reset process.
    - This API uses a **POST request**
    - Required field: `email`
    - If the user exists, a password reset email will be sent to the provided email address.
    - Rate Limit: Maximum 5 requests per minute per IP
    """

    serializer_class = ResendVerifyEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        celery_send_reset_password_mail.delay(
            user_uuid=str(user.uuid), purpose="reset_password"
        )
        return Response({"message": "check your mail , amd reset your password"})

class ResetPasswordAPI(PublicGenericAPIView):
    """
    ResetPasswordAPI is a public API for resetting user passwords.
    - This API uses a **POST request**
    - Required field: `password`
    - On successful password reset, the user's password will be updated.
    """

    serializer_class = ResetPasswordSerializer

    def post(self, request, token):
        user = verify_one_time_token(signed_token=token, purpose="reset_password")
        serializer = self.get_serializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        update_token_password(user=user, password=password)
        celery_password_reset_success_mail.delay(user_uuid=str(user.uuid))
        return Response({"message": "password update successfully"}, status=status.HTTP_200_OK)


class ChangePasswordAPI(BaseGenericApiView):
    """
    ChangePasswordAPI is a protected API for changing user passwords.
    - This API uses a **POST request**
    - Required fields: `old_password`, `new_password`
    - On successful password change, the user's password will be updated.
    """

    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user: CustomUser = request.user
        serializer = self.get_serializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get("new_password")
        update_token_password(user=user, password=new_password)
        celery_password_reset_success_mail.delay(user_uuid=str(user.uuid))
        return Response({"message": "password change successfully"}, status=status.HTTP_200_OK)


