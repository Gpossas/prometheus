from io import BytesIO
import zipfile
from django.http import HttpResponse, FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, StaleElementReferenceException, JavascriptException
import requests
import json
from django.urls import reverse

from instagram.utils import decode_and_set_cookie
from .web_driver_singleton import WebDriverSingleton
import base64

@api_view(['POST'])
def get_video( request ):
  url = request.body
  """
  get video from posts and reels\n
  return JSON:\n
  {
    name: str,
    profile_picture: str
    video_url: str
  }
  """

  user_uuid = decode_and_set_cookie(request)
  url = json.loads( request.body.decode( 'utf-8' ) ).get( 'url' )

  if user_uuid != None:
    driver = WebDriverSingleton(user_uuid)
    driver.get( url )

  for attempts in range( 3 ):
    try:
      header = driver.find_element( By.TAG_NAME, "header" )
      name = header.find_element( By.XPATH, "//header/div[2]" ).find_element( By.TAG_NAME, "a" )
      profile_picture = header.find_element( By.TAG_NAME, "img" ).get_attribute( "src" )
      video = driver.find_element( By.TAG_NAME, "video" ).get_attribute( "src" )
      
      # video image will show up in DOM when video finish execution
      driver.execute_script( 
        "video = document.querySelector('video');"
        "video.currentTime = video.duration;"
      )
      video_thumbnail = driver.find_element( By.CLASS_NAME, "x5yr21d.xl1xv1r.xh8yej3" ).get_attribute( "src" )
      break
    except ( NoSuchElementException, NoSuchAttributeException ) as e:
      return Response( {'error': f'{ e }'}, status=404 )
    except StaleElementReferenceException:
      continue
    except JavascriptException: # video didn't start automatically, video image element already in DOM
      video_thumbnail = driver.find_element( By.CLASS_NAME, "x5yr21d.xl1xv1r.xh8yej3" ).get_attribute( "src" )
      break
    except Exception as e:
      return Response( { "error": e }, status=500 )

  return Response({
    'name': name.text,
    'profile_picture': base64.urlsafe_b64encode( profile_picture.encode() ).decode(),
    'video_thumbnail': base64.urlsafe_b64encode( video_thumbnail.encode() ).decode(),
    'video_url': video,
    'proxy_server': reverse( 'api:proxy_get_image' )
  })


@api_view(['GET'])
def proxy_get_image( request, url=None ):
  if not url: return HttpResponse( "No URL" )

  image_url = base64.urlsafe_b64decode( url.encode() ).decode()
  response = requests.get( image_url )
  if response.status_code != 200:
    return HttpResponse( "Image not found" )
  
  if ( content_type := response.headers.get( 'Content-Type' ) ) == 'image/jpeg':
    image_content = response.content
    return HttpResponse( image_content, content_type=content_type )
  else:
    return HttpResponse( "Not an image" )
    

@api_view(['POST'])
def download_videos( request ):
  videos = json.loads( request.POST.get('videos', '') )
  if not videos: 
    return Response(status = 404)
  
  zip_path = './instagram/static/Prometheus.zip'
  with zipfile.ZipFile( zip_path, mode="w" ) as zip_file:
    for video in videos:
      name, video_url = video[0], video[1]
      response_object = requests.get( video_url, stream = True )

      # Create a BytesIO object to store the video data
      video_data = BytesIO()

      for chunk in response_object.iter_content( chunk_size=256 ):
        video_data.write( chunk )
      
      zip_file.writestr( ''.join( ( name,'.mp4' ) ), video_data.getvalue() )

  response = FileResponse( open( zip_path, 'rb' ), as_attachment=True, filename="Prometheus.zip" )
  return response


@api_view(['POST'])
def quit_driver( request ):
  user_uuid = decode_and_set_cookie(request)

  if user_uuid != None:
    WebDriverSingleton.close_driver(user_uuid) #only closes the driver if uuid exists
    return Response()
  else:
    return Response()