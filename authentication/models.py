from django.db import models
from django.utils import timezone
# models
from accounts.models import CustomUser

# import utils
from utils.models import BaseModel

# Create your models here.




class OneTimeToken(BaseModel):
    PURPOSE_CHOICES = [
        ("verify_email", "Email Verification"),
        ("reset_password", "Password Reset"),
        ("invite", "Invitation Link"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    token = models.CharField(max_length=255)
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and self.expired_at > timezone.now()
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.email} - {self.purpose}"
