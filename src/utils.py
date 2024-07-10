import os
import zipfile
import time 
from selenium.common.exceptions import TimeoutException
from argparse import ArgumentTypeError
import logging

def unzip_files(directory:str) -> None:
    for item in os.listdir(directory):
        if item.endswith(".zip"):  # Athuga fyrir ZIP skrá
            file_path = os.path.join(directory, item)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(directory) 
            os.remove(file_path) 

def wait_for_zip_file(download_dir, timeout=300, scan_interval=0.1):
    """
    Wait for a .zip file to appear in the specified directory.
    
    :param download_dir: Directory to monitor for the .zip file
    :param timeout: How long to wait for the .zip file (in seconds)
    :param scan_interval: How frequently to check the directory (in seconds)
    :return: The path to the downloaded .zip file
    :raises TimeoutException: If no .zip file is found within the timeout period
    """
    end_time = time.time() + timeout

    logging.info(f"Waiting for a .zip file to appear in {download_dir}...")
    
    while time.time() < end_time:
        for filename in os.listdir(download_dir):
            if filename.endswith(".zip") and not filename.endswith(".crdownload"):
                file_path = os.path.join(download_dir, filename)
                return file_path
        time.sleep(scan_interval)
    
    raise TimeoutException("Timeout waiting for the .zip file to be downloaded")

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')