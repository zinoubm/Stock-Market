from src.functions.intraday import IntradayHandler
from src.functions.dailly import DaillyHandler
from src.functions.weekly import weeklyHandler

functions = {
    "TIME_SERIES_INTRADAY": IntradayHandler,
    "TIME_SERIES_DAILY_ADJUSTED": DaillyHandler,
    "TIME_SERIES_WEEKLY": weeklyHandler,
}
