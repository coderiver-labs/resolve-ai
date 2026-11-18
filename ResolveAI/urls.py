from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include(("authentication.urls", "authentication"), namespace="authentication")),
    path("accounts/",include(("accounts.urls", "accounts"), namespace="accounts")),

]
