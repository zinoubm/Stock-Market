from src.url_manager import UrlManager


class DaillyHandler(UrlManager):
    def get_url(sefl, params):
        if params["compact"]:
            compact = "compact"
        else:
            compact = "full"

        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={params['symbol']}&apikey={params['api_key']}outputsize&={compact}"
        return url
