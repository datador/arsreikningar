import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.web_setup import setup_driver
from src.utils import unzip_files
import argparse

import time
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_ssn(ssn_list, start_year=2022):
    project_root = os.path.dirname(os.path.abspath(__file__))  # Rót verkefnisins
    #project_root = os.getcwd()  # Núverandi workdingdir
    download_dir = os.path.join(project_root, "data")  # Setja download directory innan verkefnis
    os.makedirs(download_dir, exist_ok=True)  # Búa til ef ekki til

    driver = setup_driver(download_dir)
    wait = WebDriverWait(driver, 10)
    
    for ssn in ssn_list:
        url = f"https://www.skatturinn.is/fyrirtaekjaskra/leit/kennitala/{ssn}"
        logging.info(f"getting url: {url}")
        driver.get(url)
        try:

            # Finna og smella á "show more" til að útvíkka
            collapse_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="secure" and contains(text(), "Gögn úr ársreikningaskrá")]')))
            logging.info(f"Collapse link found, about to click. {collapse_link}")
            collapse_link.click()
            logging.info(f"Fyrsti klikk takki") 
            # Bíða eftir að taflan verði sjáanleg eftir að víkkað er út
            wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@class="annualTable"]')))
            
            # Byggja XPath fyrirspurn fyrir relevant ár og data_id (ársreikninga)
            xpath_query = f'//table[@class="annualTable"]/tbody/tr[td[1][contains(text(), "{start_year}") or number(text()) > {start_year}] and td[5][@data-typeid="1"]]'
            logging.info(f"xpath query: {xpath_query}") 

            rows = driver.find_elements(By.XPATH, xpath_query)
            for row in rows:
                year_text = row.find_element(By.XPATH, './td[1]').text.strip()
                logging.info(f"Útdreginn árstexti: {year_text}") 
                
                purchase_link = row.find_element(By.XPATH, './td[5]/a[@class="tocart"]')
                purchase_link.click()
                time.sleep(5)  # Leyfa tíma fyrir vöruna að bætast við körfu ### SETJA Á XPATH/EHV ELEMENT EN EKKI SLEEP
        
        except Exception as e:
            logging.info(f"Villa við vinnslu {ssn}: {e}")
    
    # Fara í "körfu" og ljúka kaupum
    try:
        cart_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cartlink")))
        cart_link.click()
        wait.until(EC.element_to_be_clickable((By.ID, "MainContent_btnKaupa"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "MainContent_ucVoruGrid_btnSaekjaAllarVorur"))).click()
        time.sleep(2)  # Bíða eftir að zip skrániðurhal hefjist
    except Exception as e:
        logging.info(f"Villa við að ljúka kaupum: {e}")
    
    # BÍÐA EFTIR DOWNLOADI
    time.sleep(3)
    driver.quit()
    unzip_files(download_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process SSN list and start year.')
    parser.add_argument('--ssn_list', nargs='+', help='List of SSNs to process', required=True)
    parser.add_argument('--start_year', default=2022, type=int, help='Start year for filtering data', required=False)
    
    args = parser.parse_args()

    process_ssn(args.ssn_list, args.start_year)