import json

import requests

from config import API_TOKEN


class APIException(Exception):
    pass


class APIConnector:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> str:
        valid_codes = parse_supported_codes()

        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты: {base}")
        if base not in (item for sublist in valid_codes for item in sublist):
            raise APIException(f"Недопустимый код конвертируемой валюты - {base}")
        if quote not in (item for sublist in valid_codes for item in sublist):
            raise APIException(f"Недопустимый код валюты, в которую можно провести конвертацию - {quote}")
        if not amount.isdigit():
            raise APIException(f"Недопустимое количество - {amount}")
        raw_request = requests.get(
            f"https://v6.exchangerate-api.com/v6/{API_TOKEN}/pair/{base}/{quote}/{amount}",
            timeout=5,
        ).text
        return raw_request

    @staticmethod
    def get_codes() -> str:
        raw_currencies = requests.get(
            f"https://v6.exchangerate-api.com/v6/{API_TOKEN}/codes", timeout=5
        ).text
        return raw_currencies


def parse_supported_codes() -> list:
    python_currencies = json.loads(APIConnector.get_codes())
    supported_codes_list = python_currencies["supported_codes"]
    return supported_codes_list
