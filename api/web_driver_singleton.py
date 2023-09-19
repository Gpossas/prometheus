from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import platform

class WebDriverSingleton:
  _instances = {}

  def __new__( cls, token ):
    if token not in cls._instances:
      chrome_options = Options()
      chrome_options.add_argument('--headless')
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--disable-gpu')
      
      if platform.system() == "Linux": #Checking if its a linux distro
        chrome_options.binary_location = '/usr/bin/google-chrome-stable' #define the path to chrome executable file
        driver = webdriver.Chrome( options=chrome_options )
      else:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service ,options=chrome_options)
      
      driver.implicitly_wait( 15 )
      cls._instances[token] = driver

    return cls._instances[token]
  
  @classmethod
  def close_driver( cls, token ):
    if token in cls._instances:
      cls._instances[token].quit()
      del cls._instances[token]