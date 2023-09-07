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
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--disable-gpu')
      driver = webdriver.Chrome( service=Service( ChromeDriverManager().install() ), options=chrome_options )
      driver.implicitly_wait( 15 )
      cls._instance = driver
    return cls._instance
  
  @classmethod
  def close_driver( cls ):
    if cls._instance is not None:
      cls._instance.quit()
      cls._instance = None