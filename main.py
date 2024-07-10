import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.web_setup import setup_driver
from src.utils import unzip_files, wait_for_zip_file, str2bool
import argparse
from selenium.common.exceptions import TimeoutException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_ssn(ssn_list, start_year=None, path=None, unzip=True):
    if path == None:
        project_root = os.path.dirname(os.path.abspath(__file__))  # Rót verkefnisins
        #project_root = os.getcwd()  # Núverandi workdingdir
        download_dir = os.path.join(project_root, "data")  # Setja download directory innan verkefnis
        logging.info(f"Setting download_dir: {download_dir}")
        os.makedirs(download_dir, exist_ok=True)  # Búa til ef ekki til
    else:
        # Er þetta absolute path??
        if not os.path.isabs(path):
            raise ValueError(f"Path is not absolute: {path}")
        
        download_dir = os.path.normpath(path)  # Normalize the path
        logging.info(f"Setting download_dir: {download_dir}")
        os.makedirs(download_dir, exist_ok=True)

    driver = setup_driver(download_dir)
    wait = WebDriverWait(driver, 10)
    
    for ssn in ssn_list:
        url = f"https://www.skatturinn.is/fyrirtaekjaskra/leit/kennitala/{ssn}"
        logging.info(f"getting url: {url}")
        driver.get(url)
        try:

            # Finna og smella á "show more" til að útvíkka
            collapse_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="secure" and contains(text(), "Gögn úr ársreikningaskrá")]')))
            logging.debug(f"Collapse link found, about to click. {collapse_link}")
            collapse_link.click()
            # Bíða eftir að taflan verði sjáanleg eftir að víkkað er út
            wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@class="annualTable"]')))

            if start_year == None:
                years = []
                year_elements = driver.find_elements(By.XPATH, '//table[@class="annualTable"]/tbody/tr/td[1]')
                for year_element in year_elements:
                    year_text = year_element.text.strip()
                    if year_text.isdigit():
                        years.append(int(year_text))
                if years:
                    start_year = max(years)
                    logging.info(f"Latest year determined: {start_year}")
                else:
                    logging.warning("No valid years found. Skipping SSN.")
                    continue

            # Byggja XPath fyrirspurn fyrir relevant ár og data_id (ársreikninga)
            xpath_query = f'//table[@class="annualTable"]/tbody/tr[td[1][contains(text(), "{start_year}") or number(text()) > {start_year}] and td[5][@data-typeid="1"]]'
            logging.debug(f"xpath query: {xpath_query}") 

            rows = driver.find_elements(By.XPATH, xpath_query)
            try:
                for row in rows:
                    year_element = row.find_element(By.CSS_SELECTOR, 'td:first-child')
                    year = int(year_element.text.strip())
                    if year >= start_year:
                        data_type_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)')
                        if data_type_element.get_attribute('data-typeid') == '1':
                            logging.info(f"Processing year: {year}")
                            purchase_link = data_type_element.find_element(By.CSS_SELECTOR, 'a.tocart')
                            driver.execute_script("arguments[0].click();", purchase_link)
                        
            except TimeoutException:
                logging.warning(f"Timeout waiting for purchase link: {purchase_link}")
        
        except Exception as e:
            logging.info(f"General error {ssn}: {e}")
    
    # Fara í "körfu" og ljúka kaupum
    try:
        cart_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cartlink")))
        cart_link.click()
        wait.until(EC.element_to_be_clickable((By.ID, "MainContent_btnKaupa"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "MainContent_ucVoruGrid_btnSaekjaAllarVorur"))).click()
    except Exception as e:
        logging.info(f"Error in finalizing cart: {e}")
        raise

    try:
        wait_for_zip_file(download_dir, scan_interval=0.4)
    except TimeoutException as e:
        logging.info(f"Error waiting for zip file to download: {e}")
        
    if unzip:
        logging.info("unzipping files...")    
        driver.quit()
        unzip_files(download_dir)
    else:
        logging.info("Not unzipping...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process SSN list and start year.')
    parser.add_argument('--ssn_list', nargs='+', help='List of SSNs to process', required=True)
    parser.add_argument('--start_year', default=None, type=int, help='Start year for filtering data or "latest" for the most recent year', required=False)
    parser.add_argument('--path', default=None, type=str, help='Path to save the data', required=False)
    parser.add_argument('--unzip', type=str2bool, default=True, help='unzip=true unzips the data', required=False)
    
    args = parser.parse_args()

    process_ssn(args.ssn_list, args.start_year, args.path, args.unzip)