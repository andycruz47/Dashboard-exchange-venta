import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL de la página web que contiene la tabla
url = 'https://tucambista.pe/'

# Realiza la solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Asegúrate de que la solicitud fue exitosa
if response.status_code == 200:
    # Crea un objeto BeautifulSoup con el contenido de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra todas las tablas en la página
    tables = soup.find_all('table')

    # Supongamos que quieres la primera tabla (puedes ajustar esto según sea necesario)
    table = tables[0]

    # Usa pandas para leer la tabla HTML
    df = pd.read_html(str(table))[0]

    # Muestra el DataFrame
    print(df)
else:
    print(f"Error: No se pudo obtener la página. Código de estado: {response.status_code}")
