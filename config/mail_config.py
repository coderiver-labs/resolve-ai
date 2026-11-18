from decouple import config


# config mail service


MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": config("EMAIL_HOST"),
            "port": config("EMAIL_PORT", cast=int),
            "use_tls": config("EMAIL_USE_TLS", cast=bool),
            "username": config("EMAIL_HOST_USER"),
            "password": config("EMAIL_HOST_PASSWORD"),
        },
    }
}