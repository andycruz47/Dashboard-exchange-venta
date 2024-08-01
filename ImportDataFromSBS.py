from apis_sbs import ApiSBS
import pandas as pd


BASE_URL = "https://www.sbs.gob.pe"

api_consultas = ApiSBS(BASE_URL)


def getExchange(currentYear, currentMonth):
    exchanges = api_consultas.get_exchange_rate_for_month(currentYear, currentMonth)
    # Claves que deseas mantener
    keys = ['FECHA', 'MONEDA', 'VENTA']
    newKeys = {'FECHA': 'Fecha', 'MONEDA': 'Moneda', 'VENTA': 'Venta'}
    # Modificar cada diccionario en la lista
    return [{newKeys.get(k, k): v for k, v in d.items() if k in keys} for d in exchanges]

def getDataEUR(currentYear, currentMonth):
    df = pd.read_csv('exchangeHistoryEUR.csv')
    return df

'''
def getDataEUR(currentYear, currentMonth):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv('exchangeHistoryEUR.csv')
    # Consulta a la API
    currentExchanges = getExchange(currentYear, currentMonth)
    # Convertir la lista de diccionarios en un DataFrame
    dfcurrentExchanges= pd.DataFrame(currentExchanges)
    # Convertir a fecha la columna Fecha
    dfcurrentExchanges['Fecha'] = pd.to_datetime(dfcurrentExchanges['Fecha'])
    dfcurrentExchanges['Fecha'] = dfcurrentExchanges['Fecha'].dt.strftime('%Y-%m-%d')
    # Concatenar el DataFrame del CSV con el DataFrame nuevo
    return pd.concat([df, dfcurrentExchanges], ignore_index=True)
'''

def savetoCSV(currentYear, currentMonth):
    getDataEUR(currentYear, currentMonth).to_csv('ExchangeHistoryUSD.csv', index=False)
    print(f"Datos guardados en ExchangeHistoryUSD")


#print(pd.DataFrame(getExchange(2024, 7)))
#print(getDataEUR(2024, 8))
#showExchange(exchanges)
#savetoCSV(2024,8)
#print(api_consultas.get_exchange_rate_for_month(2024, 7))
#print(getExchange(2024, 7))


