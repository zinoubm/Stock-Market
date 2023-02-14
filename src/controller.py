import requests
from src.data_manager import DataManager
from src.constants import API_KEY


class Controller:
    def __init__(self):
        self.params = {
            "function": None,
            "symbol": None,
            "interval": None,
            "api_key": API_KEY,
            "adjusted": None,
            "compact": None,
            "window": None,
        }

        self.data = DataManager()
        self.url_handler = None

    def get_data(self):
        url = self.url_handler.get_url(self.params)
        print(url)
        r = requests.get(url)
        data = r.json()
        print(r.status_code)

    # def __str__(self):
    #     return f"Class::Controller\nfunction::{self.function}\nsymbol::{self.symbol}\ninterval::{self.interval}\nadjusted::{self.adjusted}\noutputsize::{self.compact}\nwindow::{self.window}"
