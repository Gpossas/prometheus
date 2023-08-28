from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
  path( '', views.get_video, name='get_video' ),
  path( 'proxy_get_image', views.proxy_get_image, name='proxy_get_image' ),
  path( 'proxy_get_image/<path:url>', views.proxy_get_image, name='proxy_get_image' ),
  path( 'download', views.download_videos, name='download_videos' ),
]