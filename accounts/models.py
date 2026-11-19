from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# base models
from accounts.base_model import BaseProfileModel

# core
from accounts.manager import UserManager

# utils 
from utils.models import BaseModel

# Create your models here.



# custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    CHOICE = [
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("user", "User"),
    ]
    
    GENDER_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Other")
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=CHOICE, null=True, blank=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    def save(self, *args, **kwargs):
        if not self._state.adding:   # means UPDATE
            old = CustomUser.objects.get(pk=self.pk)
            if old.role != self.role:
                raise ValueError("Role cannot be changed once set.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
        

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(
                fields=["role"],
                name="user_role_idx",
            ),
        ]




"""___________profiles____________"""

#  user profile model
class UserProfile(BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ["-created_at"]



#  user profile model
class StaffProfile(BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="staff_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ["-created_at"]


#  user profile model
class AdminProfile(BaseProfileModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ["-created_at"]