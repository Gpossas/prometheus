from rest_framework.response import Response
from rest_framework.decorators import api_view
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, StaleElementReferenceException
from pathlib import Path
import requests
import json
from .web_driver_singleton import WebDriverSingleton


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

  driver = WebDriverSingleton()
  url = json.loads( request.body.decode('utf-8') ).get( 'url' )
  driver.get( url )
  driver.implicitly_wait( 8 )
  try:
    header = driver.find_element( By.TAG_NAME, "header" )
    name = header.find_element( By.XPATH, "//header/div[2]" ).find_element( By.TAG_NAME, "a" )
    profile_picture = header.find_element( By.TAG_NAME, "img" ).get_attribute( "src" )
    video = driver.find_element( By.TAG_NAME, "video" ).get_attribute( "src" )
  except ( NoSuchElementException, NoSuchAttributeException ):
    return Response( {}, status=404 )
  except StaleElementReferenceException:
    return get_video( request )

  return Response({
    'name': name.text,
    'profile_picture': profile_picture,
    'video_url': video
  })

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

  driver = WebDriverSingleton()
  driver.quit()

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