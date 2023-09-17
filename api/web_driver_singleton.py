from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class WebDriverSingleton:
  _instances = {}

  def __new__( cls, user_session ):
    if user_session not in cls._instances:
      chrome_options = Options()
      chrome_options.add_argument("--headless")
      chrome_options.add_argument('--no-sandbox')
      chrome_options.add_argument('--disable-gpu')
      driver = webdriver.Chrome( service=Service( ChromeDriverManager().install() ), options=chrome_options )
      driver.implicitly_wait( 15 )
      cls._instance[user_session] = driver
    return cls._instance[user_session]
  
  @classmethod
  def close_driver( cls, user_session ):
    if user_session in cls._instances:
      cls._instances[user_session].quit()
      del cls._instances[user_session] 
