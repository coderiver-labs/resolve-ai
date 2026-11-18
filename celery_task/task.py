from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models import Q

from django.utils import timezone


# import celery
from celery import shared_task
from celery import Task

# import models 
from accounts.models import CustomUser
from authentication.models import OneTimeToken
from audit.models import AuditLog

# import tokens
from auth.tokens import create_token, generate_one_time_url

# import mail function
from utils.mail import send_email
from utils.other import get_or_none

# import utils
from typing import cast
from datetime import timedelta

# import python
from decouple import config

# account verify mail
@shared_task()
def celery_send_verify_mail(user_uuid:str, purpose:str):
    user = get_or_none(CustomUser, uuid=user_uuid)
    if not user:
        return None
    
    token = create_token(user=user, purpose=purpose)
    url = generate_one_time_url(token=token, base_url="accounts/verify-account/")
    context = {"first_name": user.first_name, "url": url}
    send_email(to=[user.email], subject="verify your account", template="emails/send_verify_email.html", context=context)




# email verify success mail sending task
@shared_task()
def celery_verify_success_mail(user_uuid:str):
    user = get_or_none(model=CustomUser,  uuid=user_uuid)
    if not user:
        return None
    subject = "Your Account verify successfully"
    template = "success_template/verify_success.html"
    login_url = f"{config("APP_BASE_URL")}{reverse('accounts:login')}"

    context = {"first_name": user.first_name, "login_url": login_url}
    send_email(to=[user.email], subject=subject, template=template, context=context)
    


# send reset password mail
@shared_task()
def celery_send_reset_password_mail(user_uuid:str, purpose:str):
    user = get_or_none(CustomUser, uuid=user_uuid)
    if not user:
        return None
    token = create_token(user=user, purpose=purpose)
    url = generate_one_time_url(token=token, base_url="accounts/reset-password/")
    send_email(to=[user.email], subject="Your password reset url", template="emails/set_new_password.html", context={"first_name": user.first_name, "url": url})



# password reset successfully
@shared_task()
def celery_password_reset_success_mail(user_uuid:str):
    user = get_or_none(CustomUser, uuid=user_uuid)
    if not user:
        return None
    subject = "Your password reset successfully"
    template = "success_template/password_change_successful.html"
    login_url = f"{config("APP_BASE_URL")}/{reverse('accounts:login')}"
    context = {"first_name": user.first_name, "login_url": login_url}
    send_email(to=[user.email], subject=subject, template=template, context=context)




# Audit log
@shared_task()
def async_log_audit(
        actor_uuid: str, ctype_id: str, object_uuid: str, 
        model_name: str, action: str, 
        before=None, after: str=None, 
        common_info: str=None, description: str=""
):
    ctype = ContentType.objects.get_for_id(ctype_id)
    common_info = common_info or {}
    
    AuditLog.objects.create(
        actor_id=actor_uuid,
        action=action,
        content_type=ctype,
        object_id=object_uuid,
        model_name=model_name,
        before=before,
        after=after,
        description=description,
        **common_info
    )





"""celery beat tasks"""
# celery beat for student fee active or inactive
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

@shared_task
def clean_JWT_tokens():
    now = timezone.now()
    seven_days_ago = now - timedelta(days=7)
    OutstandingToken.objects.filter(created_at__lt=seven_days_ago).delete()

# clean Expired onetime token
@shared_task
def clean_one_time_token():
    # hoy used na hoy expired 
    OneTimeToken.objects.filter(
        Q(is_used=True) | 
        Q(expired_at__lt=timezone.now())
    ).delete()


@shared_task
def delete_unverified_users():
    cutoff = timezone.now() - timedelta(days=1)
    CustomUser.objects.filter(
        is_verified=False,
        created_at__lt=cutoff,
    ).delete()



"""_____________________Developer Task______________"""
@shared_task()
def celery_error_task():
    print(f"Celery Error Task.")
    1 / 0

@shared_task()
def celery_success_task():
    1 + 1