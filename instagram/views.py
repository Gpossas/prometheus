from api.web_driver_singleton import WebDriverSingleton
from instagram.utils import decode_and_set_cookie

from django.shortcuts import render


def index(request):
    user_uuid = decode_and_set_cookie(request)

    if user_uuid:
        WebDriverSingleton(str(user_uuid))
    else:
        pass

    return render(request, "instagram/index.html")