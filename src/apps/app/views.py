import logging

from django.http import HttpResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request: HttpResponse):
    logger.debug("Accessed Hello world! view")
    message = "Hello world!"
    if request.user.is_authenticated:
        message = f"Hello {request.user.get_short_name()}!"

    context = {
        "message": message,
    }

    return render(request, "app/home.html", context)


def health_check(request):
    return HttpResponse(status=200)
