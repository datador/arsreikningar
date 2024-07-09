import os
import zipfile

def unzip_files(directory:str) -> None:
    for item in os.listdir(directory):
        if item.endswith(".zip"):  # Athuga fyrir ZIP skrá
            file_path = os.path.join(directory, item)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(directory) 
            os.remove(file_path) 