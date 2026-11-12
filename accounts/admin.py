from django.contrib import admin

# models 
from accounts.models import CustomUser


# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', "last_name", "email", "role", "is_verified", "is_active"]
    search_fields = ["first_name", "last_name", "email"]




