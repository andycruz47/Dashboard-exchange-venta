from typing import List, Optional
import logging
import requests


class ApisTuCambista:

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
            return response.json()
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

#https://tucambista.pe/_next/data/9LSx3oOyKjhr6cK-qe8A1/index.json
    def get_exchange_rate_today(self) -> dict:
        return self._get("_next/data/9LSx3oOyKjhr6cK-qe8A1/index.json", {})
