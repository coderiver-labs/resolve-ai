from django.contrib import admin
from authentication.models import OneTimeToken

# Register your models here.


@admin.register(OneTimeToken)
class OneTimeTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "purpose", "expired_at", "is_used"]
