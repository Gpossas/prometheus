from api.web_driver_singleton import WebDriverSingleton

from django.shortcuts import render

def index(request):
    token = request.COOKIES.get('jwt')

    if token:
        WebDriverSingleton(str(token))

    return render(request, "instagram/index.html")