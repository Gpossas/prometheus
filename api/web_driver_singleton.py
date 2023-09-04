from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class WebDriverSingleton:
  _instance = None

  def __new__( cls ):
    if cls._instance is None:
      service = webdriver.Chrome( service=Service( ChromeDriverManager().install() ) )
      cls._instance = service
    return cls._instance