from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class WebDriverSingleton:
  _instance = None

  def __new__( cls ):
    if cls._instance is None:
      chrome_options = Options()
      chrome_options.add_argument("--headless")
      service = webdriver.Chrome( service=Service( ChromeDriverManager().install() ), options=chrome_options )
      cls._instance = service
    return cls._instance