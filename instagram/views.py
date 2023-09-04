from django.shortcuts import render
from api.web_driver_singleton import WebDriverSingleton

# Create your views here.
def index( request ):
  # initiate driver
  WebDriverSingleton()
  return render( request, "instagram/index.html" )