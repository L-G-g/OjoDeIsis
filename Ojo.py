from selenium import webdriver
import time
import zipfile
import os
import glob

#Guarda el path del directorio de trabajo
patcito = os.path.realpath(os.path.dirname(__file__))

#Configuracion del WebDriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : patcito}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=options)
#Webdriver va al link de descarga
driver.get('https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre')

#Consigue el path del archivo recien descargado
list_of_files = glob.glob(patcito+"\*.zip")
latest_file = max(list_of_files, key=os.path.getctime)

#Descomprime el .zip para conseguir el .txt
with zipfile.ZipFile(latest_file, 'r') as zip_ref:
    zip_ref.extractall(patcito)