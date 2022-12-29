from selenium import webdriver
import time
import zipfile
import os
import glob
import schedule

def func():
    #Guarda el path del directorio de trabajo
    patcito = os.path.realpath(os.path.dirname(__file__))

    #Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : patcito}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(options=options)

    #Webdriver va al link de descarga
    driver.get('https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre')

    time.sleep(5)

    #Consigue el path del archivo recien descargado
    list_of_zip = glob.glob(patcito+"\*.zip")
    latest_zip = max(list_of_zip, key=os.path.getctime)

    #Descomprime el .zip para conseguir el .txt
    with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
        zip_ref.extractall(patcito)
    time.sleep(5)

    #Consigue el path del archivo recien descomprimido
    list_of_txt = glob.glob(patcito+"\*.txt")
    latest_txt = max(list_of_txt, key=os.path.getctime)
    time.sleep(5)

    #Abre el archivo .txt y consigue la linea Villa Gessell
    with open(latest_txt) as f:
        lines = f.readlines()
    f.close()

    for line in lines:
        try:
            if line.startswith(" Villa Gesell"):
                nueva_linea = line
        except:
            nueva_linea = "Sin Dato"
    time.sleep(5)

    #Escribe en un nuevo archivo la linea Villa Gesell
    with open('datita.txt', 'a') as the_file:
        the_file.write(nueva_linea)
    the_file.close()

    time.sleep(5)

    #Borra los archivos descargados
    os.remove(latest_txt)
    os.remove(latest_zip)



#Corre cada 60min
schedule.every(10).minutes.do(func)
while True:
    schedule.run_pending()
    time.sleep(1)