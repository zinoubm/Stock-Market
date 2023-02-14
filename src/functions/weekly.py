from src.url_manager import UrlManager


class weeklyHandler(UrlManager):
    def get_url(self, params):

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={params['symbol']}&apikey={params['api_key']}"
        return url
