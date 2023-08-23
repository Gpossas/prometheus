from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
  path( '', views.get_video, name='get_video' ),
  path( 'download', views.download_videos, name='download_videos' ),
]