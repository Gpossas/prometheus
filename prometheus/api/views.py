from rest_framework.response import Response
from rest_framework.decorators import api_view

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, StaleElementReferenceException
from pathlib import Path
import requests
import json


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

  #TODO: put this driver outside fuction
  driver = webdriver.Chrome( service=Service( ChromeDriverManager().install() ) ) 
  url = json.loads( request.body.decode('utf-8') ).get('url')
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
    return get_video( url )

  return Response({
    'name': name.text,
    'profile_picture': profile_picture,
    'video_url': video
  })


def download_videos( request ):
  videos = request.body

  CHUNK_SIZE = 256
  for video in videos:
    name, video_url = video['name'], video['video_url']

    response_object = requests.get( video_url, stream = True )
    file_name = "_".join( ( name, "markZuckeberkKillerTube.mp4" ) ) 
    with open( f"{ Path.home() }/Downloads/{ file_name }", "wb" ) as file: 
      for chunk in response_object.iter_content( chunk_size=CHUNK_SIZE ):
        file.write( chunk )