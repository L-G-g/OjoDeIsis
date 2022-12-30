from selenium import webdriver
import time
import zipfile
import os
import glob
import schedule
import csv
import openpyxl

patcito = os.path.realpath(os.path.dirname(__file__))
input_file = glob.glob(patcito+"\clean_datita.txt")
output_file = glob.glob(patcito+"\clean_datita.xlsx")

def func():
    """
    Esta es la funcion principal, utiliza el webdriver para conseguir el ultimo
    zip de smn, lo descomprime y guarda la linea que corresponde a la estacion
    Villa Gessell en el archivo datita.txt, si la linea es nueva se guarda tambien
    en el archivo clean_datita.txt *La idea es cambiar esto a algo mas elegante
    pero esta asi para bugfix y salvaguardar un dato por hora*
    """

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

    #Consigue la ultima linea del archivo datita.txt
    with open('datita.txt') as f:
        for line in f:
            pass
        ultima_linea = line
    
    #Escribe en un nuevo archivo la linea Villa Gesell
    with open('datita.txt', 'a') as the_file:
        the_file.write(nueva_linea)
    the_file.close()

    time.sleep(5)

    #Escribe una nueva linea en clean_datita.txt si la nueva linea es distinta a la anterior
    with open('clean_datita.txt', 'a') as the_file:
        if nueva_linea != ultima_linea:
            the_file.write(nueva_linea)
    the_file.close()
    
    #Borra los archivos descargados
    os.remove(latest_txt)
    os.remove(latest_zip)

    print("func completado", time.ctime())

def upload():
    """
    Esta funcion crea un archivo .xlsx a partir del archivo clean_datita.txt
    """

    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    headers = ["Nombre de la Estacion", "Fecha (dd-Mes-aaa)", "Horario de informe (hh:mm)", "Nubosidacion", "Visibilidad", "Temperatura", "Sensacion Termica", "Humedad", "Viento", "Presion"]

    with open(input_file[0], 'r') as data:
        reader = csv.reader(data, delimiter=';')
        ws.append(headers)
        for row in reader:
            ws.append(row)

    wb.save(output_file[0])
    print("upload completado", time.ctime())

def loop_boy():
    """
    Esta funcion corre la funcion func() cada 1 hora y la funcion
    upload() cada 1 dia.
    """

    schedule.every(60).minutes.do(func)
    schedule.every(1440).minutes.do(upload)
    while True:
        schedule.run_pending()
        time.sleep(1)

loop_boy()


