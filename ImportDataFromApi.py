from apis_net_pe import ApisNetPe
import pandas as pd
from datetime import timedelta
import csv


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


def showExchange(exchanges):
    for exchange in exchanges:
        Fecha = exchange['fecha']
        Currency = exchange['moneda']
        TCVenta = exchange['precioVenta']
        print(f'Fecha: {Fecha}')
        print(f'Moneda: {Currency}')
        print(f'Venta: {TCVenta}')
        print('--------')


def savetoCSV(exchanges, month, year):
    nameCSV = f'exchange {month}-{year}.csv'

    with open(nameCSV, mode='w', newline='') as fileCSV:
        writer = csv.writer(fileCSV)

        writer.writerow(['Fecha', 'Moneda', 'Venta'])
        
        for exchange in exchanges:
            Fecha = exchange['fecha']
            Currency = exchange['moneda']
            TCVenta = exchange['precioVenta']
            writer.writerow([Fecha, Currency, TCVenta])

    print(f"Datos guardados en {nameCSV}")


def getData(currentYear, currentMonth, lastMonth):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv('exchangeHistory.csv')
    currentExchanges = getExchange(currentYear, currentMonth)
    lastExchanges = getExchange(currentYear, lastMonth)
    # Convertir la lista de diccionarios en un DataFrame
    dfCurrentExchanges= pd.DataFrame(currentExchanges)
    dfLastExchanges= pd.DataFrame(lastExchanges)
    dfNewExchanges = pd.concat([dfLastExchanges, dfCurrentExchanges], ignore_index=True)
    #Convertir a fecha la columna Fecha
    dfNewExchanges['Fecha'] = pd.to_datetime(dfNewExchanges['Fecha'])
    #Eliminar primera fila
    dfNewExchanges = dfNewExchanges.drop(index=0)
    #Restar un dia a la fecha nueva
    dfNewExchanges['Fecha'] = dfNewExchanges['Fecha'] - timedelta(days=1)
    # Concatenar el DataFrame del CSV con el DataFrame nuevo
    return pd.concat([df, dfNewExchanges], ignore_index=True)


#print(getExchange(month, year))
#exchanges = api_consultas.get_exchange_rate_for_month(year=year, month=month)
#showExchange(exchanges)
#savetoCSV(exchanges, month, year)
#print(getData(2024, 7))


