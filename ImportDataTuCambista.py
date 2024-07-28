from apis_tu_cambista import ApisTuCambista
from dateutil import parser

BASE_URL = "https://tucambista.pe/"

api_consultas = ApisTuCambista(BASE_URL)


def getExchangeTuCambista():
    exchange = api_consultas.get_exchange_rate_today()['pageProps']['competition'][0]
    # Cambias nombres de claves
    newKeys = {'createdOn': 'Fecha', 'sellExchangeRate': 'Venta'}
    # Modificar diccionario
    newExchange = {newKeys[k]: exchange[k] for k in newKeys if k in exchange}
    newExchange['Fecha'] = parser.isoparse(newExchange['Fecha']).date().strftime("%Y-%m-%d")
    newExchange['Moneda'] = "USD"
    return newExchange


#print(getExchangeTuCambista())

