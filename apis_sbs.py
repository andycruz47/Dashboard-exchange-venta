from datetime import date, datetime
from typing import List
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd


class ApiSBS:

    #BASE_URL = "https://www.sbs.gob.pe"

    #def __init__(self, token : str None) -> None:
    #    self.token = token

    def __init__(self, BASE_URL) -> None:
        self.base_url = BASE_URL

    def _get(self, path: str, params: dict):

        #url = f"{self.BASE_URL}{path}"
        url = f"{self.base_url}{path}"

        headers = {
            #"Authorization": self.token, 
            "User-agent": "your bot 0.1"
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table')
            df = pd.read_html(str(table))[0]
            json = df.to_json(orient='records')
            return json
        elif response.status_code == 422:
            logging.warning(f"{response.url} - invalida parameter")
            logging.warning(response.text)
        elif response.status_code == 403:
            logging.warning(f"{response.url} - IP blocked")
        elif response.status_code == 429:
            logging.warning(f"{response.url} - Many requests add delay")
        elif response.status_code == 401:
            logging.warning(f"{response.url} - Invalid token or limited")
        else:
            logging.warning(f"{response.url} - Server Error status_code={response.status_code}")
        return None

    def get_exchange_rate_for_month(self, currentYear: int, currentMonth: int) -> List[dict]:
        dateInitial = date(currentYear, currentMonth, 1).strftime("%d/%m/%Y")
        dateFinal = date(currentYear, currentMonth, 31).strftime("%d/%m/%Y")
        return self._get("/app/stats/seriesH-tipo_cambio_moneda_excel.asp", {"fecha1": dateInitial, "fecha2": dateFinal, "moneda": "66"})
        #return dateInitial, dateFinal
