from src.url_manager import UrlManager


class IntradayHandler(UrlManager):
    def get_url(self, params):

        if params["adjusted"]:
            adjusted = "true"
        else:
            adjusted = "false"

        if params["compact"]:
            compact = "compact"
        else:
            compact = "full"

        url = f"https://www.alphavantage.co/query?function={params['function']}&symbol={params['symbol']}&interval={params['interval']}min&apikey={params['api_key']}&adjusted={adjusted}&outputsize={compact}"
        return url
