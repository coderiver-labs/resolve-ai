from django.http import HttpRequest

# import rest framework
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError

# import python standard library 
import hashlib


# create your validators here.




"""refresh token validator"""
from auth.authentication import check_validate_refresh_token
def validate_refresh_token(request:HttpRequest):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        raise ValidationError("Refresh Token Not Found")        
        
    return check_validate_refresh_token(refresh_token=refresh_token)


"""access token validator""" 
def validate_access_token(request: HttpRequest) -> AccessToken:
    """
    Validate access token from cookie.
    Raises AuthenticationFailed on missing, expired or invalid token.
    """
    token = request.COOKIES.get("access_token")
    if not token:
        raise AuthenticationFailed("Authentication token was not found. Please log in.")
    try:
        return AccessToken(token)
    except ExpiredTokenError:
        raise AuthenticationFailed("Access token expired.")

    except (InvalidToken, TokenError):
        raise AuthenticationFailed("Invalid access token.")



def get_valid_user(user) :
    """
    Ensure user is active and verified.
    """
    if not user.is_active:
        raise AuthenticationFailed("User account is inactive.")
    if not getattr(user, "is_verified", True):
        raise AuthenticationFailed("User account is not verified.")
    return user


"""one time token validator"""
def verify_one_time_token(signed_token: str, purpose: str):
    """
    Verify a one-time token for a specific purpose.
    """
    from accounts.models import OneTimeToken
    token_hash = hashlib.sha256(signed_token.encode()).hexdigest()

    try:
        obj = OneTimeToken.objects.get(token=token_hash, purpose=purpose)
    except OneTimeToken.DoesNotExist:
        raise ValidationError("Invalid or malformed token")
    
    if obj.is_used:
        raise ValidationError("Token has already been used")
    if not obj.is_valid():
        raise ValidationError("Token has expired or is no longer valid")
    
    obj.is_used = True
    obj.save(update_fields=["is_used"])
    return obj.user

