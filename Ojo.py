from selenium import webdriver
import time
import zipfile
import os
import glob
import schedule
import csv
import openpyxl
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import wget
import logging
print("Es el logging")


print("entro")
patcito = os.path.realpath(os.path.dirname(__file__))
input_file = glob.glob(patcito+"/clean_datita.txt")
output_file = glob.glob(patcito+"/clean_datita.xlsx")

print(patcito)
print(input_file)
print(output_file)


def func():
    """
    Esta es la funcion principal, utiliza el webdriver para conseguir el ultimo
    zip de smn, lo descomprime y guarda la linea que corresponde a la estacion
    Villa Gessell en el archivo datita.txt, si la linea es nueva se guarda tambien
    en el archivo clean_datita.txt *La idea es cambiar esto a algo mas elegante
    pero esta asi para bugfix y salvaguardar un dato por hora*
    """


    """
    #Configuracion del WebDriver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : patcito}
    options.add_experimental_option("prefs",prefs)
    options.headless = True
    driver = webdriver.Chrome(options=options)
    #Webdriver va al link de descarga
    driver.get('https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre')

    time.sleep(5)
    """
    print("Consiguiendo .zip")
    wget.download('https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre', out = "/home/OjoDeIsis")
    print(".zip conseguido")

    #Consigue el path del archivo recien descargado
    list_of_zip = glob.glob(patcito+"/*.zip")
    latest_zip = max(list_of_zip, key=os.path.getctime)
    print("path del  lastest_zip", latest_zip)
    #Descomprime el .zip para conseguir el .txt
    with zipfile.ZipFile(latest_zip, 'r') as zip_ref:
        zip_ref.extractall(patcito)
    print(".zip Extraido")

    #Consigue el path del archivo recien descomprimido
    list_of_txt = glob.glob(patcito+"/*.txt")
    latest_txt = max(list_of_txt, key=os.path.getctime)

    print("Path del .txt conseguido")

    #Abre el archivo .txt y consigue la linea Villa Gessell
    with open(latest_txt, errors = "replace") as f:
        lines = f.readlines()
    
    nueva_linea = "Sin dato"
    for line in lines:
        if line.startswith(" Villa Gesell"):
            nueva_linea = line
    print("Nueva Linea conseguida")
    print("la nueva linea es", nueva_linea)

    #Consigue la ultima linea del archivo datita.txt
    with open('/home/OjoDeIsis/datita.txt', errors = "replace") as f:
        for linea in f:
            pass
        ultima_linea = linea
    print("Ultima Linea conseguida", ultima_linea)

    #Escribe en un nuevo archivo la linea Villa Gesell
    with open('/home/OjoDeIsis/datita.txt', 'a', errors = "replace") as the_file:
        the_file.write(nueva_linea)
    the_file.close()

    print("datita.txt modificada")

    #Escribe una nueva linea en clean_datita.txt si la nueva linea es distinta a la anterior
    with open('/home/OjoDeIsis/clean_datita.txt', 'a', errors = "replace") as the_file:
        if nueva_linea != ultima_linea:
            the_file.write(nueva_linea)
    the_file.close()
    print("clean_datita.txt modificada")

    #Borra los archivos descargados
    os.remove(latest_txt)
    os.remove(latest_zip)
    print("Archivos removidos")
    print("func() completado")

def upload():
    """
    Esta funcion crea un archivo .xlsx a partir del archivo clean_datita.txt
    """

    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    headers = ["Nombre de la Estacion", "Fecha (dd-Mes-aaa)", "Horario de informe (hh:mm)", "Nubosidacion", "Visibilidad", "Temperatura", "Sensacion Termica", "Humedad", "Viento", "Presion"]

    with open(input_file[0], 'r', errors = "replace") as data:
        reader = csv.reader(data, delimiter=';')
        ws.append(headers)
        for row in reader:
            ws.append(row)

    wb.save(output_file[0])
    print("clean_datita.xlsx generado")

    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("/home/OjoDeIsis/mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    print("GoogleDrive funcionando")

    folder_title = "Test_Isis"
    folder_id = '1iussAmgNbUWp5FgXpAg2580NBwqlmd-K'

    # 2) Retrieve the folder id - start searching from root
    file_list = drive.ListFile({'q': "'1iussAmgNbUWp5FgXpAg2580NBwqlmd-K' in parents and trashed=false"}).GetList()
    for file in file_list:
        if(file['title'] == folder_title):
            folder_id = file['id']
            break

    # 3) Build string dynamically (need to use escape characters to support single quote syntax)
    str = "\'" + folder_id + "\'" + " in parents and trashed=false"    

    # 4) Starting iterating over files
    file_list = drive.ListFile({'q': str}).GetList()
    for file in file_list:
        file1 = drive.CreateFile({'id': file["id"]})
        file1.Trash()  # Move file to trash.
        file1.UnTrash()  # Move file out of trash.
        file1.Delete()

    print("Archivo viejo eliminado")

    gfile = drive.CreateFile({'parents': [{'id': '1iussAmgNbUWp5FgXpAg2580NBwqlmd-K'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile("/home/OjoDeIsis/clean_datita.xlsx")
    gfile.Upload() # Upload the file.

    print("Archivo nuevo subido")

    print("upload() terminado")

def loop_boy():
    """
    Esta funcion corre la funcion func() cada 1 hora y la funcion
    upload() cada 1 dia.
    """

    schedule.every(60).minutes.do(func)
    schedule.every(60).minutes.do(upload)
    while True:
        schedule.run_pending()
        time.sleep(1)

func()
upload()
print("func() y upload() terminados")
#loop_boy()
