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

time.sleep(1)

#Consigue el path del archivo recien descargado
list_of_zip = glob.glob(patcito+"\*.zip")
latest_zip = max(list_of_zip, key=os.path.getctime)

#Descomprime el .zip para conseguir el .txt
with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
    zip_ref.extractall(patcito)

#Consigue el path del archivo recien descomprimido
list_of_txt = glob.glob(patcito+"\*.txt")
latest_txt = max(list_of_txt, key=os.path.getctime)

#Abre el archivo .txt y consigue la linea Villa Gessell
with open(latest_txt) as f:
    lines = f.readlines()
f.close()
for line in lines:
    if line.startswith(" Villa Gesell"):
        nueva_linea = line

#Escribe en un nuevo archivo la linea Villa Gesell
with open('datita.txt', 'a') as the_file:
    the_file.write(nueva_linea)
the_file.close()

#Borra los archivos descargados
os.remove(latest_txt)
os.remove(latest_zip)