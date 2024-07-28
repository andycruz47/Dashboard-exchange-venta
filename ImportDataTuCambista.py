from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

def getExchangeTuCambista(url):
    # Configurar opciones para Selenium
    options = Options()
    options.headless = True

    #service = Service(executable_path=os.path.join('chrome-headless-shell-win64', 'chrome-headless-shell.exe'))
    service = Service(executable_path=os.path.join('chromedriver.exe'))

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
            
    # Esperar a que la tabla esté presente
    wait = WebDriverWait(driver, 2)
    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
            
    # Extraer la tabla
    html_table = table.get_attribute('outerHTML')
    df = pd.read_html(html_table)[0]
    return df['Venta'][0]
