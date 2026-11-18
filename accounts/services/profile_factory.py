from rest_framework.request import HttpRequest
from rest_framework.exceptions import ValidationError

# import models 
from accounts.models import CustomUser, UserProfile, StaffProfile, AdminProfile

# import audit
from audit.services import AuditService


# create profile factory


def create_user_profile(user: CustomUser, request: HttpRequest):
    profile = UserProfile.objects.create(user=user)
    AuditService.create_log(actor=request.user, instance=profile, request=request, description="User Profile Created")
    return profile

def create_staff_profile(user: CustomUser, request: HttpRequest):
    profile = UserProfile.objects.create(user=user)
    AuditService.create_log(actor=request.user, instance=profile, request=request, description="User staff Created")
    return profile

def create_admin_profile(user: CustomUser, request: HttpRequest):
    profile = UserProfile.objects.create(user=user)
    AuditService.create_log(actor=request.user, instance=profile, request=request, description="User admin Created")
    return profile





class ProfileFactory:

    REGISTRY = {
        "user": create_user_profile,
        "staff": create_staff_profile,
        "admin": create_admin_profile,
    }

    @classmethod
    def create(cls, user: CustomUser, request: HttpRequest):
        creator = cls.REGISTRY.get(user.role)

        if not creator:
            raise ValidationError(
                f"Unsupported role: {user.role}"
            )

        return creator(user=user, request=request)