from apis_net_pe import ApisNetPe
import pandas as pd
from time import sleep
from datetime import timedelta

BASE_URL = "https://api.apis.net.pe"

api_consultas = ApisNetPe(BASE_URL)

# Api Consulta reniec dni 
#print(api_consultas.get_person("46027897"))
# Api Consulta ruc sunat
#print(api_consultas.get_company("10460278975"))
# Api consulta tipo de cambio del dia sunata
#print(api_consultas.get_exchange_rate_today())
# Api sunat tipo de cambio en sunat para una fecha especifica
#exchange = api_consultas.get_exchange_rate("2024-07-15")
# Consulta de api sunat - tipo de cambio de un mes en especifico
#print(api_consultas.get_exchange_rate_for_month(month=7, year=2024))


def getExchange(year, month):
    exchanges = api_consultas.get_exchange_rate_for_month(year=year, month=month)
    # Claves que deseas mantener
    keys = ['fecha', 'moneda', 'venta']
    newKeys = {'fecha': 'Fecha', 'moneda': 'Moneda', 'venta': 'Venta'}
    # Modificar cada diccionario en la lista
    return [{newKeys.get(k, k): v for k, v in d.items() if k in keys} for d in exchanges]

def getDataUSD(currentYear, currentMonth):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv('exchangeHistoryUSD.csv')
    # Espera 1 segundo
    sleep(1)
    # Consulta a la API
    currentExchanges = getExchange(currentYear, currentMonth)
    # Convertir la lista de diccionarios en un DataFrame
    dfcurrentExchanges= pd.DataFrame(currentExchanges)
    # Convertir a fecha la columna Fecha
    dfcurrentExchanges['Fecha'] = pd.to_datetime(dfcurrentExchanges['Fecha']).dt.date
    # Restar un dia a la fecha nueva
    dfcurrentExchanges['Fecha'] = dfcurrentExchanges['Fecha'] - timedelta(days=1)
    # Concatenar el DataFrame del CSV con el DataFrame nuevo
    return pd.concat([df, dfcurrentExchanges], ignore_index=True)

def savetoCSV(currentYear, currentMonth):
    getDataUSD(currentYear, currentMonth).to_csv('ExchangeHistoryUSD.csv', index=False)
    print(f"Datos guardados en ExchangeHistoryUSD")

#print(pd.DataFrame(getExchange(2024, 7)))
#print(getDataUSD(2024, 8))
#showExchange(exchanges)
#savetoCSV(2024,8)
#print(getDataUSD(2024, 7))


