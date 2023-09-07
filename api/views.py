from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, StaleElementReferenceException, JavascriptException
from pathlib import Path
import requests
import json
from django.urls import reverse
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
  print('get video starting...')
  url = json.loads( request.body.decode( 'utf-8' ) ).get( 'url' )
  driver = WebDriverSingleton()
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
      return Response( {"error": e }, status=500 )

  return Response({
    'name': name.text,
    'profile_picture': base64.urlsafe_b64encode( profile_picture.encode() ).decode(),
    'video_thumbnail': base64.urlsafe_b64encode( video_thumbnail.encode() ).decode(),
    'video_url': video,
    'proxy_server': reverse( 'api:proxy_get_image' )
  })


@api_view(['GET'])
def proxy_get_image( request, url=None ):
  if not url: return HttpResponse("No URL")

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
  videos = json.loads( request.body.decode('utf-8') )
  if not videos: 
    return Response(status = 404)
  
  CHUNK_SIZE = 256
  directory_path = create_directory_path()

  for video in videos:
    name, video_url = video[0], video[1]

    response_object = requests.get( video_url, stream = True )
    file_name = "_".join( ( name, "prometheus.mp4" ) ) 
    with open( f"{ directory_path }/{ file_name }", "wb" ) as file: 
      for chunk in response_object.iter_content( chunk_size=CHUNK_SIZE ):
        file.write( chunk )

  return Response()


@api_view(['POST'])
def quit_driver( request ):
  WebDriverSingleton.close_driver()
  return Response()


def create_directory_path():
  directory_path = f"{ Path.home() }/Downloads/Prometheus"
  while os.path.exists( directory_path ):
    start = directory_path.find( '(' )
    end = directory_path.find( ')' )
    if start == -1 and end == -1:
      directory_path = ' '.join( ( directory_path, '(1)' ) )
    else:
      counter = int( directory_path[start + 1: end] )
      directory_path = directory_path.replace( f"({ counter })", f"({ counter + 1 })" )
  os.mkdir( directory_path )
  return directory_path