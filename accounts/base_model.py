from django.db import models
from utils.models import BaseModel

# create base model

class BaseProfileModel(BaseModel):
    GENDER_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Other")
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True