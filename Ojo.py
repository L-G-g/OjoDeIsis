from selenium import webdriver
import time
import zipfile
import os



options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.path.realpath(os.path.dirname(__file__))}

options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(chrome_options=options)

driver.get('https://ssl.smn.gob.ar/dpd/zipopendata.php?dato=tiepre')

time.sleep(5)

#with zipfile.ZipFile(__file__, 'r') as zip_ref:
#    zip_ref.extractall(__file__)