
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def setup_driver(download_dir):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Reyna nota local ChromeDriver first, annars sækja..
    # Hægt að ná í hér: https://googlechromelabs.github.io/chrome-for-testing/#stable
    chrome_driver_path = "C:/repos/rsk/chromedriver/chromedriver.exe" ## breyta í dýnamískt path frá rót
    if os.path.exists(chrome_driver_path):
        service = Service(chrome_driver_path)
    else:
        # Fall back á ChromeDriverManager ef local driver finnst ekki
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    return driver