from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.request import Request, HttpRequest
from rest_framework import status

# Sentry
import sentry_sdk

# import logger and sentry
import sentry_sdk
import logging
logger = logging.getLogger("error")

# create exception handler


def custom_exception_handler(exc: Exception, context: dict):

    response = exception_handler(exc, context)

    # Expected errors
    if response is not None:
        return Response(
            {
                "success": False,
                "status_code": response.status_code,
                "errors": response.data,
            },
            status=response.status_code,
        )

    # Unexpected error → capture to Sentry
    request: HttpRequest = context.get("request")

    with sentry_sdk.push_scope() as scope:

        if request:
            if hasattr(request, "user") and request.user.is_authenticated:
                scope.set_user({
                    "id": str(request.user.uuid),
                })

            scope.set_extra(
                "request_id",
                getattr(request, "request_id", None),
            )

            scope.set_extra("path", request.path)
            scope.set_extra("method", request.method)

        sentry_sdk.capture_exception(exc)

    # Structured logging
    logger.error(
        "Unhandled server error",
        extra={
            "action": "unhandled_exception",
            "error_type": exc.__class__.__name__,
        },
        exc_info=True,
    )

    # Safe generic response
    return Response(
        {
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "errors": {
                "detail": "Something went wrong on server.",
            },
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )